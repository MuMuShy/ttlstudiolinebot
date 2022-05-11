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
class Bot():
    def __init__(self,bot:LineBotApi):
        self.linebotapi = bot
    
    def getUserMessage(self,event):
        _userText = event.message.text
        _userId = event.source.user_id
        self.linebotapi.reply_message(
            event.reply_token,
            TextSendMessage(text=_userText+"id:"+_userId)
        )

if __name__ == "__main__":
    pass