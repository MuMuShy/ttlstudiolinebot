import os
import random
import psycopg2
from dotenv import load_dotenv
import time
load_dotenv()
DATABASE_URL = os.environ['DATABASE_URL']
class DataBase():
    def __init__(self):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    
    def createUser(self,user_line_id,user_line_name):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="""INSERT INTO users (user_line_name, user_line_id) VALUES (%(user_line_name)s, %(user_line_id)s)"""
        params = {'user_line_name':user_line_name, 'user_line_id':user_line_id}
        self.cursor.execute(sql,params)
        self.conn.commit()
    
    def checkUser(self,user_line_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="SELECT user_line_id FROM users where user_line_id = '"+user_line_id+"'"
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        # 事物提交
        self.conn.commit()
        if row is not None:
            return True
        else:
            return False
    
    #確認玩家是否有輸入序號
    def checkUserIsInGame(self,user_line_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="SELECT user_line_id,serial_number FROM opengame_list where user_line_id = '"+user_line_id+"'"
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        # 事物提交
        self.conn.commit()
        if row is not None:
            json = {"user_line_id":row[0],"serial_number":row[1]}
            return True,json
        else:
            return False,None
    
    def addOpenGame(self,user_line_id,serial_number):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        try:
            sql ="""INSERT INTO opengame_list (user_line_id, serial_number) VALUES (%(user_line_id)s, %(serial_number)s)"""
            params = {'user_line_id':user_line_id, 'serial_number':serial_number}
            self.cursor.execute(sql,params)
            self.conn.commit()
            return True
        except:
            return False
    
    def SetSerialNumberValid(self,serial_number,is_valid):
        #設定序號是否過期
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        #try:
        if is_valid is True:
            is_valid = "TRUE"
        else:
            is_valid = "FALSE"
        sql ="UPDATE serial_numbers SET is_valid = '{is_valid}' WHERE serial_number = '{serial_number}'".format(is_valid = is_valid,serial_number = serial_number)
        self.cursor.execute(sql)
        self.conn.commit()
        return True
        #
    
    def addSerialNumber(self,serial_number,expiration_time):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        try:
            sql ="""INSERT INTO serial_numbers (serial_number, expiration_time) VALUES (%(serial_number)s, %(expiration_time)s)"""
            params = {'serial_number':serial_number, 'expiration_time':expiration_time}
            self.cursor.execute(sql,params)
            self.conn.commit()
            print("產生新序號:"+serial_number)
            return True
        except:
            return False
    
    def getSerialNumberInfo(self,serialNumber):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="SELECT serial_number,expiration_time FROM serial_numbers where serial_number ='"+serialNumber+"'"
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        # 事物提交
        self.conn.commit()
        print(row)
        _data = {"serail_number":row[0],"expiration_time":row[1]}
        return _data
    
    def getSerialNumberList(self):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="SELECT serial_number,expiration_time FROM serial_numbers"
        self.cursor.execute(sql)
        row = self.cursor.fetchall()
        # 事物提交
        self.conn.commit()
        print(row)
        json = []
        for serial in row:
            _data = {"serail_number":serial[0],"expiration_time":serial[1]}
            json.append(_data)
        return json

if __name__ == "__main__":
    database = DataBase()
    database.SetSerialNumberValid("S63rWM20",False)