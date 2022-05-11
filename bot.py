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
import tools
from database import DataBase
from datetime import datetime, timedelta
import math
class Bot():
    def __init__(self,bot:LineBotApi,dataBase:DataBase):
        self.linebotapi = bot
        self.database = dataBase
    
    def getUserMessage(self,event):
        _userText = event.message.text
        
        if _userText == "!cs":
            self.createSerialNumber(event)
        elif _userText == "!ls":
            self.listSerialNumbers(event)
        elif _userText =="!play":
            self.playGame(event)
        elif _userText.startswith("!start"):
            serial_number = tools.checkSerialInput(_userText)
            if serial_number is not None:
                self.openGame(event,serial_number)
            else:
                self.linebotapi.reply_message(
                    event.reply_token,
                    TextSendMessage(text="序號輸入格式有問題")
                )


    def createSerialNumber(self,event):
        print("產生新序號")
        _life_time_seconds = 3600 #序號有效時間
        _randomSerial = tools.random_str(5)
        current_time = datetime.now()
        final_time = current_time+timedelta(seconds=_life_time_seconds)
        final_time = (final_time.strftime("%m/%d/%Y %H:%M:%S"))
        _toDatabase = self.database.addSerialNumber(_randomSerial,final_time)
        if _toDatabase is True:
            self.linebotapi.reply_message(
                event.reply_token,
                TextSendMessage(text="成功產生序號:"+_randomSerial+"\n到期時間:"+final_time)
            )
        else:
            self.linebotapi.reply_message(
                event.reply_token,
                TextSendMessage(text="產生序號發生問題 請聯絡管理員")
            )
        
    
    def listSerialNumbers(self,event):
        print("列出序號&過期時間")
        _all_serial = self.database.getSerialNumberList()
        _reply = ""
        for serial in _all_serial:
            _reply+="序號:"+serial["serail_number"]+"\n"+"過期時間"+serial["expiration_time"]+"\n"
        self.linebotapi.reply_message(
            event.reply_token,
            TextSendMessage(text=_reply)
        )
    
    def checkSerialNumberIsLegal(self,serial_number):
        serial_info = self.database.getSerialNumberInfo(serial_number)
        _finaltime = datetime.strptime(serial_info["expiration_time"],"%m/%d/%Y %H:%M:%S")
        time_elapsed = (_finaltime - datetime.now())
        time_elapsed = math.floor(time_elapsed.total_seconds())
        #如果過期時間減去目前時間 小於等於0 代表序號已過期
        if time_elapsed <= 0:
            return False
        else:
            return True
    
    #進行遊戲
    def playGame(self,event):
        _userId = event.source.user_id
        user_is_ingame,info = self.database.checkUserIsInGame(_userId)
        #玩家已在遊戲中 檢查序號是否過期
        if user_is_ingame is True:
            serial_number = info["serial_number"]
            if self.checkSerialNumberIsLegal(serial_number) is False:
                self.linebotapi.reply_message(
                    event.reply_token,
                    TextSendMessage(text="您好,您的序號已過期,請輸入新的序號開通遊戲")
                )
                return
            #進入遊戲邏輯 
            else:
            #----------------------------------
                self.linebotapi.reply_message(
                    event.reply_token,
                    TextSendMessage(text="遊玩邏輯")
                )
        else:
            self.linebotapi.reply_message(
                event.reply_token,
                TextSendMessage(text="您好,您目前沒有開通任何遊戲,請輸入 !start 序號 進行開通 序號為英數字組合,請洽管理員")
            )
    
    #開通遊戲
    def openGame(self,event,serial_number):
        _userId = event.source.user_id
        print("open game")
        #先確認玩家是否已經在遊戲中
        user_is_ingame,info = self.database.checkUserIsInGame(_userId)
        if user_is_ingame is True:
            self.linebotapi.reply_message(
                event.reply_token,
                TextSendMessage(text="目前您已有開通遊戲囉")
            )
            return
        #先確認序號是否合法 並且沒有過期
        if self.checkSerialNumberIsLegal(serial_number) is True:
            result = self.database.addOpenGame(_userId,serial_number)
            if result is True:
                self.linebotapi.reply_message(
                    event.reply_token,
                    TextSendMessage(text="成功開通遊戲! 可以使用 !play 開始")
                )
            else:
                self.linebotapi.reply_message(
                    event.reply_token,
                    TextSendMessage(text="開通遊戲失敗 請假管理員")
                )
        else:
            self.linebotapi.reply_message(
                event.reply_token,
                TextSendMessage(text="序號失效,請洽管理員")
            )
    



    










if __name__ == "__main__":
    pass