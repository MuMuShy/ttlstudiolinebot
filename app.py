import random
from time import sleep, time
from flask import Flask, request,abort
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
from database import DataBase
from bot import Bot

app = Flask(__name__)

environment = os.getenv("ENVIRONMENT")
gm = os.getenv("U8d0f4dfe21ccb2f1dccd5c80d5bb20fe")
print("environment: "+environment)

if environment =="DEV":
    print("本地開發 使用本地開發版本機器人")
    line_bot_api = LineBotApi(os.getenv("LINE_BOT_API_DEV"))
    handler = WebhookHandler(os.getenv("LINE_BOT_SECRET_DEV"))  
else:
    print("線上heroku環境 預設線上版機器人")
    line_bot_api = LineBotApi(os.getenv("LINE_BOT_API"))
    handler = WebhookHandler(os.getenv("LINE_BOT_SECRET"))
database = DataBase()
#創建class
bot =  Bot(line_bot_api,database)

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
    print("收到訊息")
    print(event)
    #基礎判斷 過濾一些沒加好友的 回傳加好友訊息
    checkUserResult = checkUserData(event)
    if checkUserResult is True:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="第一次傳送訊息,已成功創建資料 請再次傳送指令")
        )
        return
    elif checkUserResult is False:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="看來你沒有加我好友! 請先加我好友喔")
        )
        return
    #驚嘆號開頭 進入bot基本功能邏輯
    if event.message.text.startswith("!"):
        bot.getUserMessage(event)
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="無指令"))

def checkUserData(event):
    user_id = event.source.user_id
    try:
        profile = line_bot_api.get_profile(user_id)
    except:
        return False
    if database.checkUser(user_id) is True:
        print("玩家有資料 checkuser通過")
    else:
        user_line_name = profile.display_name
        database.createUser(user_id,user_line_name)
        return True
        




if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    if environment =="DEV":
        app.run(host='0.0.0.0', port=port)
    else:
        app.run(host='0.0.0.0', port=port)
    