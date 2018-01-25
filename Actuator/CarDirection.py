#!/usr/bin/env python
import PCA9685 as servo
import time                # Import necessary modules

def Map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class CarDirection():
	"""docstring for CarDirection"""
	def __init__(self):
		self.leftPWM = 400
		self.homePWM = 450
		self.rightPWM = 500
		self.offset =0
		try:
			for line in open('config'):
				if line[0:8] == 'offset =':
					self.offset = int(line[9:-1])
		except:
			print 'config error'
		self.leftPWM += self.offset
		self.homePWM += self.offset
		self.rightPWM += self.offset
		self.pwm = servo.PWM()                  # Initialize the servo controller.
		self.pwm.frequency = 60

	# ==========================================================================================
	# Control the servo connected to channel 0 of the servo control board, so as to make the 
	# car turn left.
	# ==========================================================================================
	def turn_left(self):
		self.pwm.write(0, 0, self.leftPWM)  # CH0

	# ==========================================================================================
	# Make the car turn right.
	# ==========================================================================================
	def turn_right(self):
		self.pwm.write(0, 0, self.rightPWM)

	# ==========================================================================================
	# Make the car turn back.
	# ==========================================================================================

	def turn(self, angle):
		angle = Map(angle, 0, 255, self.leftPWM, self.rightPWM)
		self.pwm.write(0, 0, angle)

	def home(self):
		self.pwm.write(0, 0, self.homePWM)

	def calibrate(self, x):
		self.pwm.write(0, 0, 450+x)

