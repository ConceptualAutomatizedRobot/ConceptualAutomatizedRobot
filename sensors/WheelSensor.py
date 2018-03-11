import RPi.GPIO as GPIO
import time

from threading import Thread

import sys
sys.path.insert(0,"../system/")
from system import System

class WheelSensor(Thread):
	"""docstring for WheelSensor"""
	def __init__(self,system, nb_tics_by_turn = 2):
		Thread.__init__(self)
		self.system = system
		self.on = True

		self.nb_tics_by_turn = nb_tics_by_turn
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

	def wait_for(self, distance):
		buffer = 0
		nb_tics = (distance / 21.0) * self.nb_tics_by_turn
		print(nb_tics)
		i = 0
		etat = 0

		while i<nb_tics:
			time.sleep(0.001)
			buffer = (buffer << 1) | GPIO.input(36)
			if (buffer & 0b1111) == 0b1111 :
				if etat == 0:
					i +=1
					print(i)
					etat = 1
			elif (buffer & 0b1111) == 0b0000 :
				etat = 0

	def run(self):
		while self.on:
			GPIO.wait_for_edge(36,GPIO.RISING)
			tS = time.time()
			GPIO.wait_for_edge(36,GPIO.RISING)
			tE = time.time()

			# self.system.notify({"type":System.E_SPEED,"value":10.5/(tE-tS)})
			t = tE - tS # temps pour faire 1/2 tour de roue
			self.system.notify({"type":System.E_SPEED,"value":t})
			time.sleep(0.1)

	def stop(self):
		self.on = False