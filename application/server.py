#!/usr/bin/python
#-*- coding: utf-8 -*-

from threading import Thread
import xmlrpc
from xmlrpc.server import SimpleXMLRPCServer

import sys
sys.path.insert(0,"../system/")
from system import System
from event import Event

class Server(Thread):

	_server = None
	_system = None
	_run = True

	PILOT_MODE = 0
	SUIVI_MODE = 1
	PARCOURS_MODE = 2

	def __init__(self,system = None):
		Thread.__init__(self)

		self._server = SimpleXMLRPCServer(("",8028), allow_none = True, use_builtin_types=True)
		self._server.register_introspection_functions()

		print(self._server.server_address[0])
		self._system = system

	def getPort(self):
		return self._server.server_address[1]

	def setSpeed(self,speed):
		print("setSpeed")
		self._system.setSpeed(speed)
		return 0

	def getSpeed(self):
		return self._system.getSpeed()

	def stop(self):
		print("stop")
		self._system.stop()
		self._run = False
		return 0

	def setMotor(self,direction):
		print("setDirection")
		if direction == 1:
			self._system.motorForward()
		elif direction == -1:
			self._system.motorBackward()
		elif direction == 0:
			self._system.motorStop()
		return 0

	def setAngle(self,angle):
		print("setAngle")
		self._system.setAngle(angle)

	def setMode(self,mode):
		print("setMode")
		if mode == PILOT_MODE:
			self._system.notify(Event(System.E_METH,self._system.F_GUIDE))
		elif mode == SUIVI_MODE:
			self._system.notify(Event(System.E_METH,self._system.F_FOLLOW))
		elif mode == PARCOURS_MODE:
			self._system.notify(Event(System.E_METH,self._system.F_PARKOUR))
		return 0

	# def addTarget(self,name,target):
	# 	print("addTarget")
	# 	self._system.addTarget([name,target])
	# 	return 0

	def setTarget(self, data):
		print("setTarget")
		self._system.setTarget(data)
		return 0

	def moveCamera(self,direction):
		print("moveCamera")
		self._system.moveCamera(direction)
		return 0

	def cameraHome(self):
		print("cameraHome")
		self._system.cameraHome()
		return 0

	def setCoord(self, latitude, longitude):
		print("setCoord")
		self._system.parkourTo(latitude, longitude)
		return 0


	def run(self):
		self._server.register_function(self.setSpeed,'setSpeed')
		self._server.register_function(self.getSpeed,'getSpeed')
		self._server.register_function(self.setMotor,'setMotor')
		self._server.register_function(self.setAngle,'setAngle')
		self._server.register_function(self.moveCamera,'moveCamera')
		self._server.register_function(self.cameraHome,'cameraHome')

		self._server.register_function(self.setMode,'setMode')
		self._server.register_function(self.setTarget,'setTarget')
		self._server.register_function(self.setCoord,'setCoord')

		self._server.register_function(self.stop,'stop')

		# self._system.start()

		while self._run:
			self._server.handle_request()





if __name__ == "__main__":
	import time
	import signal
	import socket

	def signal_handler(signal, frame):
		print("Pressed ctrl+C")
		st.stop()
		exit(0)

	signal.signal(signal.SIGINT, signal_handler)

	st = System()
	Sergei = Server(st)
	# Sergei = Server()
	Sergei.start()

	# s = xmlrpclib.ServerProxy('http://127.0.1.1:'+str(Sergei.getPort()),allow_none=True)

	# time.sleep(1)
	# s.stop()

	print("Press Ctrl+C to stop")
	signal.pause()

	st.join()
	Sergei.join()