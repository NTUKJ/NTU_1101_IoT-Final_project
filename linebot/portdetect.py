import sys
import glob
import serial
import re

uid_pattern = re.compile(r'Card UID: (.+)')

def serial_ports():
		if sys.platform.startswith('win'):
			ports = ['COM%s' % (i + 1) for i in range(256)]
		elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
			ports = glob.glob('/dev/tty[A-Za-z]*')
		elif sys.platform.startswith('darwin'):
			ports = glob.glob('/dev/tty.*')
		else:
			raise EnvironmentError('Unsupported platform')

		for port in ports:
			try:
				s = serial.Serial(port,9600)
				msg = s.readline().decode('utf-8')
				if "Firmware Version" in msg:
					s.close()
					print('FOUND:', port)
					return port
				else:
					print("close")
					s.close()
			except (OSError, serial.SerialException):
				pass
			except KeyboardInterrupt:
				break

if __name__ == '__main__':
		port_opened = serial_ports()
		s = serial.Serial(port_opened,9600)
		try:
			while True:
				msg = s.readline().decode('utf-8')
				tmp = re.match(uid_pattern, msg)
				if tmp:
					uid = "".join(str(tmp.group(1)).split(" "))
					print(uid)
		except KeyboardInterrupt:
			s.close()
			print("Program Closed")
			pass