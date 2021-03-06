#!/usr/bin/env python3
# coding: utf-8

import RPi.GPIO as GPIO
import time
from threading import Thread

import sys
sys.path.insert(0,"../system/")
from system import System

class DistanceSensor(Thread):
	"""docstring for DistanceSensor"""
	def __init__(self, trigPin = 40, echoPin = 38, mod = GPIO.BOARD):
		""" Constructeur - Permet de crer un sonard 

			:param trigPin: numero du pin corresspondant au triger -1 if the triger isn't set by this class
			:param echoPin: numero du pin corresspondant à l'echo
			:param mod: mod d'addressage du bord soit en GPIO.BORD soit en GPIO.BCM
		"""
		print("mod : " + str(mod))
		GPIO.setmode(mod)
		self.Trig = trigPin
		self.Echo = echoPin
		self.mod  = mod

		GPIO.setup(self.Trig,GPIO.OUT)
		GPIO.setup(self.Echo,GPIO.IN)

		GPIO.output(self.Trig, False)

	def getDistance(self):
		self.trigerMesure()
		return self.mesuring()

	def cleanup(self):
		GPIO.cleanup()

	def mesuring(self):
		""" 
			Fonction en attente d'un signal trigger afin d'effectuer la mesure 
	
		"""
		#GPIO.setmode(self.mod)
		## Emission de l'ultrason
		#while GPIO.input(self.Echo)==0:  
		GPIO.wait_for_edge(self.Echo, GPIO.RISING)
		debutImpulsion = time.time()

		## Retour de l'Echo
		#while GPIO.input(self.Echo)==1:   
		GPIO.wait_for_edge(self.Echo, GPIO.FALLING)
		finImpulsion = time.time()


		

		distance = round((finImpulsion - debutImpulsion) * 340 * 100 / 2, 1)  ## Vitesse du son = 340 m/s

		print(distance)
		return distance

	def trigerMesure(self):
		GPIO.output(self.Trig, True)
		time.sleep(0.00001)
		GPIO.output(self.Trig, False)


	def trigerMesurePWMmesurPerSeconds(self, nbMesurePerSecond):
			""" 
				Permet de configurer une pin en pwm 
				afin qu'elle effecue le nombre de mesusre souhaité
				:param nbMesurePerSecond: Nombre de mesure à effectuer par secondes
			"""
			pass

	def trigerMesurePWM(self, dc = 1, freq = 1):
		"""
			Utiliser cette fonction pour déclancher une mesure par le bié de la pin 12
			du raspberry pi 3 qui elle seule peut générer un signale PWM
			Pour cela il faut brancher le triger du sonard sur le pin 12
			
			:param dc: Duty cyce ( 0.0 <= dc <= 100.0)
			:param freq: Frequence du pwm
		"""
		#try:
			#GPIO.setmode(GPIO.BOARD)
			#GPIO.setup(self.Trig, GPIO.OUT)

		self.p=GPIO.PWM(self.Trig, freq)

<<<<<<< HEAD:Sensor/DistanceSensor.py
		self.p.start(dc)
		print(" Triger Setted ")
		"""except KeyboardInterrupt:
			print(" Exiting program")
		except:
			print(" Other exception detected\n"+str(sys.exc_info()[0]) )
		finally:
			GPIO.cleanup()
			p.stop()"""

	def stopMesurePwm(self):
		self.p.stop()


def main():
	dSens = DistanceSensor(12,18)
	dSens.trigerMesurePWM()
	try:
		while(1):
			dSens.mesuring()
	except KeyboardInterrupt:
		print(" Exiting program")
	except:
		print(" Other exception detected\n"+str(sys.exc_info()[0]) )
	finally:
		dSens.cleanup()
	"""dSens.trigerMesurePWM()
	while(1):
		print(dSens.mesuring())"""
if __name__ =='__main__':
	main()
=======
	def stop(self):
		self.on = False

	def run(self):
		while self.on:
			time.sleep(0.1)
			d = self.getDistance()
			self.system.notify({"type":System.E_DIST,"value":d})

	def __del__(self):
		GPIO.cleanup()
>>>>>>> acbded5c76bec1c3d23f619d8bd33606ead831f8:sensors/DistanceSensor.py
