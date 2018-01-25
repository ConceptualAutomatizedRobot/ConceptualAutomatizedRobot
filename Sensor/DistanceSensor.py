import RPi.GPIO as GPIO
import time

class DistanceSensor():
	"""docstring for DistanceSensor"""
	def __init__(self):
		GPIO.setmode(GPIO.BOARD)

		self.Trig = 40
		self.Echo = 38

		GPIO.setup(self.Trig,GPIO.OUT)
		GPIO.setup(self.Echo,GPIO.IN)

		GPIO.output(self.Trig, False)

	def getDistance(self):
		GPIO.output(self.Trig, True)
		time.sleep(0.00001)
		GPIO.output(self.Trig, False)

		while GPIO.input(self.Echo)==0:  ## Emission de l'ultrason
			debutImpulsion = time.time()

		while GPIO.input(self.Echo)==1:   ## Retour de l'Echo
			finImpulsion = time.time()

		distance = round((finImpulsion - debutImpulsion) * 340 * 100 / 2, 1)  ## Vitesse du son = 340 m/s

		return distance

	def cleanup(self):
		GPIO.cleanup()