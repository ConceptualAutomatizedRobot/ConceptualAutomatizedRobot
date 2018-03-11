#!/usr/bin/env python3
# coding: utf-8

import serial 
import termios, sys
from micropyGPS import MicropyGPS
import time
################################################################################
# https://github.com/inmcm/micropyGPS #
################################################################################


class Gps:

	_fd = -1;
	_my_gps = None

	def __init__(self):
		self.configure_serial()
		"""if self._fd != -1:
			serialClose(self._fd)"""



	def read_next(self):
		buf=['\0']
		var = True

		iNeedDollar = '$'
		while iNeedDollar != self._fd.read():
			pass
		#buf.append(iNeedDollar)
		buf = [iNeedDollar]+buf

		while var:
			#buf[len(buf)-1]=iNeedDollar
			buf[len(buf)-1] = self._fd.read()
			if buf[len(buf)-1] == '\r':
				buf[len(buf)-1] = '\n'
			buf.append('\0')
			if (len(buf) > 2 and  buf[len(buf)-2] == '\n' and buf[len(buf)-3] == '\n'):
				self._my_gps = MicropyGPS()
				my_sentence=''.join(buf)
				for x in my_sentence:
					self._my_gps.update(x)
				var = False
			#print(self._fd.read())
		print(''.join(buf))

	def longitude(self):
		return self._my_gps.longitude

	def latitude(self):
		return self._my_gps.latitude



	def configure_serial(self):
		self._fd = serial.Serial(
    	port='/dev/ttyS0',
    	baudrate=9600#,
    	#parity=serial.PARITY_ODD,
    	#stopbits=serial.STOPBITS_TWO,
    	#bytesize=serial.SEVENBITS
		)
		optionFlag = termios.tcgetattr(self._fd)
		optionFlag[2] &= ~termios.PARENB
		optionFlag[2] &= ~termios.CSTOPB
		optionFlag[2] &= ~termios.CSIZE
		optionFlag[2] |=  termios.CS8
		optionFlag[3] &= ~(termios.ICANON | termios.ECHO | termios.ECHOE | termios.ISIG)
		optionFlag[1] &= ~termios.OPOST
		optionFlag[2] |= (termios.CLOCAL | termios.CREAD)

		#cfsetispeed(&options, B9600)
		#cfsetospeed(&options, B9600)

		termios.tcsetattr(self._fd, termios.TCSANOW, optionFlag)

		message = "$PMTK314,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*%x\r\n"
		#print(self.crc(message))
		buffer  = message%self.crc(message)
		#buffer  = message%18
		print(buffer)
		
		print(" Sended Bytes :"+str(self._fd.write(str.encode(buffer)))) # TODO à vérifier 
		#print(" Sended Bytes :" + str(self._fd.write(buffer))) # TODO à vérifier 

	def crc(self, message):
		res = 0
		#res = np.array([0], dtype='uint8')
		i=1
		while message[i] != '*':
			res ^= ord(message[i])
			i+=1
		return res


