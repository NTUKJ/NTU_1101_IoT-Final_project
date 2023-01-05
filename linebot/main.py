from re import match
from datetime import date, datetime, timedelta
import time, psycopg2, os
from portdetect import * 
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

def update_table_row(DATABASE_URL, uid, nowTime):
	
	print('\n','-'*20)
	print('uid =',uid, 'nowTime',nowTime)
	
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cursor = conn.cursor() # 初始化執行指令的工具

	cursor.execute("UPDATE pig_care SET LastEatTime = %s WHERE rfid = %s;", (str(nowTime), uid))
	print("Updated 1 row of data")

	conn.commit()
	cursor.close()
	conn.close()

def Fetch_table_row(DATABASE_URL):

	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cursor = conn.cursor() # 初始化執行指令的工具

	cursor.execute("SELECT * FROM pig_care;")
	rows = cursor.fetchall()

	# Print all rows
	# for row in rows:
	# 	print("Data row = (%s, %s, %s)" %(str(row[0]), str(row[1]), str(row[2])))

	conn.commit()
	cursor.close()
	conn.close()

	return rows

def check_table_row(DATABASE_URL, line_bot_api, ckeck_time_warning):

	print('\nChecking table row...')
	rows = Fetch_table_row(DATABASE_URL)

	nowTime = datetime.now()
	text_info = ''
	for row in rows:

		rfid = row[1]
		past_time = datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S.%f")
		duration = (nowTime - past_time).seconds

		if duration > ckeck_time_warning:
			text = '-'*20 + '\nWarning\nID：「'+str(rfid)+'」 \nAbnormal diet about '+ str(duration) + ' seconds!\n'
			# print(text)
			text_info += text

	print(text_info)
	if text_info != []:
		line_bot_api.push_message('U70d4875c22240836332561cc9485826c', TextSendMessage(text=text_info))
	print('='*80)

if __name__ == '__main__':

	DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a kj-iot2').read()[:-1]
	line_bot_api = LineBotApi('A/lZF7guXu0wk/Vryza9qVhKO1CxPSQyLdsLlrEtmf/vnMYuX5bABO4JWWcDcPQ17vOPTZC/jgOV788AG71YP1IvlWiI++11UN5VljRLMgJBOQGU8CrmCjciD67WlPQ+g8GTY4Vc6j4tX/Y5sIzNegdB04t89/1O/w1cDnyilFU=')
	port_opened = serial_ports()
	s = serial.Serial(port_opened, 9600, timeout = 0.1)
	tic = time.clock()

	try:
		while True:
			# print('-')
			msg = s.readline().decode('utf-8')
			tmp = re.match(uid_pattern, msg)
			if tmp:
				uid = "".join(str(tmp.group(1)).split(" "))
				uid = str(uid.split("\r")[0])
				nowTime = datetime.now()
				update_table_row(DATABASE_URL, uid, nowTime)

			if time.clock()-tic > 60:

				check_table_row(DATABASE_URL, line_bot_api, ckeck_time_warning = 15)

				tic = time.clock()

				

	except KeyboardInterrupt:
		s.close()
		print("Program Closed")
		