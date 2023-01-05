from re import match
import pandas as pd
from datetime import date, datetime, timedelta
import time
import csv
from portdetect import * 

CHECK_TIME_INTERVAL = 30 # minutes 

# df2 = pd.DataFrame(columns=['LastEatTime', 'RFID'])

# new_pig = {'LastEatTime':datetime.now(), 'RFID':'0xFF'}
# new_pig1 = {'LastEatTime':datetime(2022, 1, 1, 4, 35, 25), 'RFID':'0xFD'}
# new_pig2 = {'LastEatTime':datetime(2022, 1, 2, 4, 38, 25), 'RFID':'807B781C'}
# df2 = df2.append(new_pig, ignore_index=True)
# df2 = df2.append(new_pig1, ignore_index=True)
# df2 = df2.append(new_pig2, ignore_index=True)
# df2 = df2.set_index("RFID")

# now = datetime(2022, 1, 1, 4, 35, 25)
# diff = datetime.now() - now
# print(diff.days)

# df2.to_csv('df2.csv')

# read_df2 = pd.read_csv('df2.csv')
# print(read_df2)

# for i in range(read_df2.shape[0]):
# 	tmp = datetime.strptime(read_df2['LastEatTime'][i], '%Y-%m-%d %H:%M:%S.%f')
# 	print((datetime.now() - tmp).days)



if __name__ == '__main__':
	read_df = pd.read_csv('./df2.csv')
	checkTime = datetime(2022, 1, 1, 4, 35, 25)
	# time_interval = datetime.now() - checkTime
	# print(time_interval)
	# print(time_interval.seconds//3600)
	print(read_df)
	port_opened = serial_ports()
	s = serial.Serial(port_opened,9600)
	try:
		while True:
			msg = s.readline().decode('utf-8')
			tmp = re.match(uid_pattern, msg)
			if tmp:
				uid = "".join(str(tmp.group(1)).split(" "))
				uid = str(uid.split("\r")[0])
				print(uid)
				# print(read_df['RFID'].str.match(uid))
				if uid in read_df.values:
					print("exist")
					match_row = read_df.index[read_df['RFID'] == uid].tolist()
					match_row = int(match_row[0])
					lastEatTime = datetime.strptime(read_df.iloc[match_row]['LastEatTime'], '%Y-%m-%d %H:%M:%S.%f')
					# print("how many days not eat:",(datetime.now() - lastEatTime).days)
					read_df.loc[match_row,['LastEatTime']] = datetime.now()
					read_df.to_csv('df2.csv',index=False)
				else:
					print("not Exist")
					new_pig = {'LastEatTime':datetime.now(), 'RFID': uid}
					read_df = read_df.append(new_pig, ignore_index=True)
					read_df.to_csv('df2.csv',index=False)

				read_df = pd.read_csv('./df2.csv')
				print(read_df)

			time_interval = datetime.now() - checkTime
			time_interval = time_interval.seconds//3600
			time_interval = int(str(time_interval))
			# print((datetime.now() - checkTime))
			if time_interval > 0:
				for i in range(read_df.shape[0]):
					tmp = datetime.strptime(read_df['LastEatTime'][i], '%Y-%m-%d %H:%M:%S.%f')
					print("pig",i,": ",(datetime.now() - tmp).days)
				checkTime = datetime.now()

	except KeyboardInterrupt:
		s.close()
		print("Program Closed")
		