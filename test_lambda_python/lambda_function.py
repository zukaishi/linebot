import os, sys, json
import requests
from linebot import (LineBotApi, WebhookHandler)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)
from linebot.exceptions import (LineBotApiError, InvalidSignatureError)

line_bot_api = LineBotApi(os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])

def lambda_handler(event, context):
    print(event)
    signature = event["headers"]["x-line-signature"]
    body = event["body"]

    ok_json = os.environ["ok_json"]
    error_json = os.environ["error_json"]

    # weather
    url = "https://community-open-weather-map.p.rapidapi.com/weather"
    querystring = {"q":"Tokyo,jp","units":"metric","lang":"ja"}
    headers = {
        'x-rapidapi-key': os.environ["X_RAPIDAPI_KEY"],
        'x-rapidapi-host': os.environ["X_RAPIDAPI_HOST"]
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)
    
    @handler.add(MessageEvent, message=TextMessage)
    def message(line_event):
        text = line_event.message.text
        line_bot_api.reply_message(line_event.reply_token, TextSendMessage(text=text)) 

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