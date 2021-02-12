import os, sys, json, datetime,time 
import requests
from linebot import (LineBotApi, WebhookHandler)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)
from linebot.exceptions import (LineBotApiError, InvalidSignatureError)
from pytz import timezone

line_bot_api = LineBotApi(os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])

def lambda_handler(event, context):
    print(event)
    signature = event["headers"]["x-line-signature"]
    body = event["body"]

    ok_json = os.environ["ok_json"]
    error_json = os.environ["error_json"]

    @handler.add(MessageEvent, message=TextMessage)
    def message(line_event):
        #text = line_event.message.text
        text = getWeather()
        line_bot_api.reply_message(line_event.reply_token, TextSendMessage(text=text)) 

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
        words = '【今日の天気】\n'
        # JST = timezone(timedelta(hours=+9), 'JST')
        for item in forecastData['list']:
            forecastDatetime = timezone('Asia/Tokyo').localize(datetime.datetime.fromtimestamp(item['dt']))

            if item['dt'] < time.time() or item['dt'] > (time.time()  + 86400):
                break

            weatherDescription = item['weather'][0]['description']
            emoji = ''
            # 絵文字の分岐は適当
            if '曇' in weatherDescription or '雲' in weatherDescription:
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
            words += '\n{0}\n天気:{1} {2}\n気温(℃):{3}\n雨量(mm):{4}\n'.format(item['dt'], emoji, weatherDescription, temperature, rainfall)
        
        return words

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