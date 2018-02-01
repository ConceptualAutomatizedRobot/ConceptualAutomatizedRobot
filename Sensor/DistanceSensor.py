#!/usr/bin/env python3
# coding: utf-8

import RPi.GPIO as GPIO
import time

class DistanceSensor():
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
		#while GPIO.input(self.Echo)==0:  ## Emission de l'ultrason
		GPIO.add_event_detect(self.Echo, GPIO.RISING)
		debutImpulsion = time.time()

		#while GPIO.input(self.Echo)==1:   ## Retour de l'Echo
		GPIO.add_event_detect(self.Echo, GPIO.FAILLING)
		finImpulsion = time.time()

		distance = round((finImpulsion - debutImpulsion) * 340 * 100 / 2, 1)  ## Vitesse du son = 340 m/s

		return distance

	def trigerMesure(self):
		GPIO.output(self.Trig, True)
		time.sleep(0.00001)
		GPIO.output(self.Trig, False)
