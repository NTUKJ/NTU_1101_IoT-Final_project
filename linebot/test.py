import os
import psycopg2
import datetime


DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a kj-iot').read()[:-1]

def create_table(DATABASE_URL):

	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cursor = conn.cursor() # 初始化執行指令的工具

	create_table_query = '''CREATE TABLE pig_care(
							id serial PRIMARY KEY,
							rfid VARCHAR(50),
							lastEatTime VARCHAR(50)
							);'''  # SQL 指令做成字串物件

	cursor.execute(create_table_query) # 執行
	# print("Finished creating table")

	conn.commit() # 確認執行
	cursor.close()
	conn.close()


def init_table(DATABASE_URL):

	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cursor = conn.cursor() # 初始化執行指令的工具

	nowTime = datetime.datetime.now()
	cursor.execute("INSERT INTO pig_care (rfid, LastEatTime) VALUES (%s, %s);", ("fake_id_1", '2022-01-10 12:00:00.0'))
	cursor.execute("INSERT INTO pig_care (rfid, LastEatTime) VALUES (%s, %s);", ("fake_id_2", '2022-01-10 12:00:00.0'))
	cursor.execute("INSERT INTO pig_care (rfid, LastEatTime) VALUES (%s, %s);", ("807B781C", str(nowTime)))
	cursor.execute("INSERT INTO pig_care (rfid, LastEatTime) VALUES (%s, %s);", ("315165D9", str(nowTime)))
	# print("Inserted 4 rows of data")

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


def update_table_row(DATABASE_URL):

	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cursor = conn.cursor() # 初始化執行指令的工具

	nowTime = datetime.datetime.now()
	cursor.execute("UPDATE pig_care SET LastEatTime = %s WHERE rfid = %s;", (str(nowTime), "807B781C"))
	# print("Updated 1 row of data")

	conn.commit()
	cursor.close()
	conn.close()

def check_table_row():

	nowTime = datetime.datetime.now()
	for row in rows:

		rfid = row[1]
		past_time = datetime.datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S.%f")
		duration = (nowTime - past_time).seconds
		text_info = 'ID：「'+str(rfid)+'」| Abnormal diet about '+ str(duration) + 'seconds!'
		if duration > 5:

			line_bot_api.push_message('U70d4875c22240836332561cc9485826c', TextSendMessage(text=text_info))