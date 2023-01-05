from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


#======這裡是呼叫的檔案內容=====
from message import *
from new import *
from Function import *
#======這裡是呼叫的檔案內容=====

#======python的函數庫==========
import tempfile, os, re
import datetime
import time
import psycopg2
from urllib.parse import urlparse
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi('A/lZF7guXu0wk/Vryza9qVhKO1CxPSQyLdsLlrEtmf/vnMYuX5bABO4JWWcDcPQ17vOPTZC/jgOV788AG71YP1IvlWiI++11UN5VljRLMgJBOQGU8CrmCjciD67WlPQ+g8GTY4Vc6j4tX/Y5sIzNegdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('e755ec351e78012112aa037adbeaa097')
# DATABASE URL
DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a kj-iot2').read()[:-1]


# User ID
# 主動推撥 (每月500則)
line_bot_api.push_message('U70d4875c22240836332561cc9485826c', TextSendMessage(text='App start!!'))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
    # handler.handle(body, signature)
        while 1:
        
            url = urlparse.urlparse(os.environ.get('DATABASE_URL'))
            db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)
            conn = psycopg2.connect(db)

            # conn = psycopg2.connect(DATABASE_URL, sslmode='require')

            cursor = conn.cursor() # 初始化執行指令的工具
            cursor.execute("SELECT * FROM pig_care;")
            rows = cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()

            nowTime = datetime.datetime.now()
            for row in rows:

                rfid = row[1]
                past_time = datetime.datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S.%f")
                duration = (nowTime - past_time).seconds
                text_info = 'ID：「'+str(rfid)+'」| Abnormal diet about '+ str(duration) + 'seconds!'
                if duration > 5:

                    line_bot_api.push_message('U70d4875c22240836332561cc9485826c', TextSendMessage(text=text_info))
            

            time.sleep(30)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
        
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text
    if re.match('告訴我秘密',message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage('才不告訴你哩！'))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))

# 主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
