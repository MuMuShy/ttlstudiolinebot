import random
from time import sleep, time
from flask import Flask, request, abort
from flask import render_template
from dotenv import load_dotenv
import math
from datetime import datetime, timedelta
load_dotenv()
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,PostbackEvent,ImageSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,FlexSendMessage
)
import os

app = Flask(__name__)


environment = os.getenv("ENVIRONMENT")
print("environment: "+environment)

local_storage={}
limite_user={}
if environment =="DEV":
    print("本地開發 使用本地開發版本機器人")
    line_bot_api = LineBotApi(os.getenv("LINE_BOT_API_DEV"))
    handler = WebhookHandler(os.getenv("LINE_BOT_SECRET_DEV"))  
else:
    print("線上heroku環境 預設線上版機器人")
    line_bot_api = LineBotApi(os.getenv("LINE_BOT_API"))
    handler = WebhookHandler(os.getenv("LINE_BOT_SECRET"))


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


#用戶post訊息
@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    if data.startswith("@auctionAddequipment"):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=data))
        return

#用戶文字訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="測試測試"))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    if environment =="DEV":
        app.run(host='0.0.0.0', port=port)
    else:
        app.run(host='0.0.0.0', port=port)
    