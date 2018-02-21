#!/usr/bin/python
#-*- coding: utf-8 -*-

#Import classe Moteur & Direction

import time
from threading import Thread

import sys
from log import Logfile

import os

# Actuators
sys.path.insert(0,"../actuators/")
from Motor import Motor
from CarDirection import CarDirection
from VideoDirection import VideoDirection

class Event(object):

	def __init__(self,type,value):
		self.type = type
		self.value = value

	def __str__(self):
		return "type : "+str(self.type)+", value : "+str(self.value)


class System(Thread):

	E_DIST = "d"
	E_SPEED = "s"
	E_XPOS = "x"
	E_YPOS = "y"
	E_CMD = "c"
	E_METH = "m"

	P_LEFT = -1
	P_RIGHT = 1
	P_MIDDLE = 0

	P_UP = 1
	P_BOTTOM = -1

	F_HOME = "home"
	F_FOLLOW = "follow"
	F_PARKOUR = "parkour"
	F_GUIDE = "guide"

	_motor = None
	_direction = None
	_log = None
	_camera = None

	_vars = None
	_methods = None

	_speed = 50

	#DIRECTION_CAMERA
	DIRECTION_LEFT = 0
	DIRECTION_LEFT_UP = 1
	DIRECTION_UP = 2
	DIRECTION_UP_RIGHT = 3
	DIRECTION_RIGHT = 4
	DIRECTION_RIGHT_DOWN = 5
	DIRECTION_DOWN = 6
	DIRECTION_DOWN_LEFT = 7

	_path = None


	def __init__(self):
		Thread.__init__(self)
		
		self._motor = Motor()
		self._direction = CarDirection()
		self._camera = VideoDirection()

		self._path = os.getcwd()
		self._log = Logfile(self._path+"/logs")
		self._imagePath = self._path+"/image"

		self._methods = {System.F_HOME:self.home, System.F_FOLLOW:self.follow, System.F_PARKOUR:self.parkour, System.F_GUIDE:self.guide}
		self._vars = {System.E_DIST:100, System.E_SPEED:0, System.E_XPOS:System.P_MIDDLE, System.E_YPOS:System.P_MIDDLE , System.E_METH:System.F_HOME}
		self._on = True

	def run(self):
		self.home()
		
		while self._on:
			self._motor.setSpeed(self._speed)
			methode = self._methods[self._vars[System.E_METH]]
			methode()

		self._log.write("Car stop")
		self._motor.stop()

	def home(self):
		print("Home")
		self._direction.home()
		self._camera.home()

	def parkour(self):
		print("Parkour")
		
#		if len(self._targets) > 0 :
#			target = self._targets.pop[0]
#			# Recherche de la cible
#
#			# Aller à la cible
#			reached = False
#			while !reached:
#				

#		else :
#			print("No targets")
#			if self._vars[System.E_POS] < System.P_MIDDLE:
#				self._direction.turn_left()
#				self._log.write("direction turn_left")
#			elif self._vars[System.E_POS] > System.P_MIDDLE:
#				self._direction.turn_right()
#				self._log.write("direction turn_right")
#			else :
#				self._direction.home()
#				self._log.write("direction home")

	def guide(self):
		print("Guide")
		time.sleep(1)

	def follow(self):
		self._motor.forward()
		# Block vitesse
		if self._vars[System.E_DIST] <= 10:
			self._motor.backward()
			self._log.write("Motor backward")
		elif self._vars[System.E_DIST] <= 20:
			self._motor.stop()
			self._log.write("Motor stop")
		else :
			self._motor.forward()
			self._log.write("Motor forward")

		#Block direction
		if self._vars[System.E_XPOS] == System.P_LEFT:
			self._direction.turn_left()
			self._log.write("direction turn_left")
		elif self._vars[System.E_XPOS] == System.P_RIGHT:
			self._direction.turn_right()
			self._log.write("direction turn_right")
		else :
			self._direction.home()
			self._log.write("direction home")

		time.sleep(0.2)

	def target_found(self):
		self._found = True

	def notify(self, event):
		self._vars[event.type] = event.value
		self._log.write(event)

		# target : tuple[name,img]
	def addTarget(self,target):
		self._targets.append(target)

	def stop(self):
		self._on = False

	def getSpeed(self):
		return self._vars[System.E_SPEED]

	#	Direction externe
	def motorStop(self):
		self._motor.stop()

	def setSpeed(self,speed):
		self._speed = speed
		self._motor.setSpeed(speed)

	def motorForward(self):
		self._motor.forward()

	def motorBackward(self):
		self._motor.backward()

	def setAngle(self,angle):
		self._direction.turn(angle)

	def moveCamera(self,direction):
		if direction == self.DIRECTION_LEFT:
			self._camera.move_decrease_x()
		elif direction == self.DIRECTION_LEFT_UP:
			self._camera.move_decrease_x()
			self._camera.move_increase_y()
		elif direction == self.DIRECTION_UP:
			self._camera.move_increase_y()
		elif direction == self.DIRECTION_UP_RIGHT:
			self._camera.move_increase_y()
			self._camera.move_increase_x()
		elif direction == self.DIRECTION_RIGHT:
			self._camera.move_increase_x()
		elif direction == self.DIRECTION_RIGHT_DOWN:
			self._camera.move_increase_x()
			self._camera.move_decrease_y()
		elif direction == self.DIRECTION_DOWN:
			self._camera.move_decrease_y()
		elif direction == self.DIRECTION_DOWN_LEFT:
			self._camera.move_decrease_x()
			self._camera.move_decrease_y()

	def cameraHome(self):
		self._camera.home_x_y()

	def setTarget(self, data):
		try:
			with open(self._imagePath, 'wb') as file:
				file.write(data)
				file.close()
		except Exception as e:
			print(e)
		

	def parkourTo(self, lat, long):
		print("ARRRRRRRMEN")

if __name__ == "__main__":
	sylvain = System()

	sylvain.start()

	#time.sleep(1)
	#sylvain.notify(Event(System.E_METH,System.F_FOLLOW))
	#time.sleep(1)
	#sylvain.notify(Event(System.E_DIST,15))
	#time.sleep(1)
	#sylvain.notify(Event(System.E_DIST,5))
	#time.sleep(1)
	#sylvain.notify(Event(System.E_DIST,30))
	#time.sleep(1)


	sylvain.motorForward()
	time.sleep(0.2)

	sylvain.stop()
	sylvain.join()

	print("Stop")