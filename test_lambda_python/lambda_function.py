import boto3
import os, sys, json,time,datetime
import requests
import pprint
from linebot import (LineBotApi, WebhookHandler)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)
from linebot.exceptions import (LineBotApiError, InvalidSignatureError)
from pytz import timezone
from datetime import timedelta,timezone

line_bot_api = LineBotApi(os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])

def lambda_handler(event, context):
    ok_json = os.environ["ok_json"]
    error_json = os.environ["error_json"]

    def getWeather():
        url = "https://community-open-weather-map.p.rapidapi.com/forecast"
        querystring = {"q":"Tokyo,jp","units":"metric","lang":"ja"}
        headers = {
            'x-rapidapi-key': os.environ["X_RAPIDAPI_KEY"],
            'x-rapidapi-host': os.environ["X_RAPIDAPI_HOST"]
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        print(response.text)
        forecastData = json.loads(response.text)
        print(forecastData)

        if not ('list' in forecastData):
            print('error')
            return
        
        # 通知内容作成
        words = 'この後の天気はこんな感じだかっぱ\n'
        JST = timezone(timedelta(hours=+9), 'JST')
        for item in forecastData['list']:
            if item['dt'] < time.time() or item['dt'] > (time.time()  + 86400):
                break

            weatherDescription = item['weather'][0]['description']
            emoji = ''
            
            if '薄い雲' in weatherDescription:
                emoji = '\uDBC0\uDCAC\uDBC0\uDCA9'
            elif '曇' in weatherDescription or '雲' in weatherDescription:
                emoji = '\uDBC0\uDCAC'
            elif '雪' in weatherDescription:
                emoji = '\uDBC0\uDCAB'
            elif '雨' in weatherDescription:
                emoji = '\uDBC0\uDCAA'
            elif '晴' in weatherDescription:
                emoji = '\uDBC0\uDCA9'
    
            temperature = item['main']['temp']
            rainfall = 0
            if 'rain' in item and '3h' in item['rain']:
                rainfall = item['rain']['3h']
            words += '\n{0}\n天気:{1} {2}\n気温(℃):{3}\n雨量(mm):{4}\n'.format(datetime.datetime.fromtimestamp(item['dt'], JST), emoji, weatherDescription, temperature, rainfall)
        
        return words

    @handler.add(MessageEvent, message=TextMessage)
    def message(line_event):
        text = line_event.message.text
        if '天気' in line_event.message.text:
            text = getWeather()
        line_bot_api.reply_message(line_event.reply_token, TextSendMessage(text=text)) 

    print(event)


    mode = 'weather'
    body = ''
    # ユーザ決定
    if "headers" in event:
        signature = event["headers"]["x-line-signature"]
        body = event["body"]
        d = json.loads(body)
        user = d["events"][0]["source"]["userId"] 
    else:
        user = 'test'

    dynamoDB = boto3.resource("dynamodb")
    table = dynamoDB.Table("kappa_mode")
    dt_now = datetime.datetime.now()
    last_time = dt_now.strftime('%Y/%m/%d %H:%M:%S')

    response = table.get_item(
        Key={'user': user, 'mode': mode}
    )
    if "Item" in response:
        item = response["Item"]
        if item["status"] == 1:
             table.put_item(
                Item = {
                    "user": user,
                    "mode": mode,
                    "status": 2,
                    "last_time": last_time
                }
            )
    else:
        table.put_item(
            Item = {
                "user": user,
                "mode": mode,
                "status": 1,
                "last_time": last_time
            }
        )

    if body:
        try:
            handler.handle(body, signature)
        except LineBotApiError as e:
            logger.error("Got exception from LINE Messaging API: %s\n" % e.message)
            for m in e.error.details:
                logger.error("  %s: %s" % (m.property, m.message))
            return error_json
        except InvalidSignatureError:
            return error_json
    return ok_json