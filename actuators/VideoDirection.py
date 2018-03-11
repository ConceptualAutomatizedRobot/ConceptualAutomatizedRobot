#!/usr/bin/env python
import PCA9685 as servo
import time                  # Import necessary modules

class VideoDirection():

	MinPulse = 200
	MaxPulse = 700

	Current_x = 0
	Current_y = 0

	pas = 10

	"""docstring for VideoDirection"""
	def __init__(self):
		self.offset_x = 0
		self.offset_y = 0
		try:
			for line in open('config'):
				if line[0:8] == 'offset_x':
					self.offset_x = int(line[11:-1])
					#print 'offset_x =', offset_x
				if line[0:8] == 'offset_y':
					self.offset_y = int(line[11:-1])
					#print 'offset_y =', offset_y
		except:
			pass
		self.Xmin = self.MinPulse + self.offset_x
		self.Xmax = self.MaxPulse + self.offset_x
		self.Ymin = self.MinPulse + self.offset_y
		self.Ymax = self.MaxPulse + self.offset_y
		self.home_x = (self.Xmax + self.Xmin)/2
		self.home_y = (self.Ymax + self.Ymin)/2 -25#self.Ymin + 80
		self.pwm = servo.PWM()                  # Initialize the servo controller.
		self.pwm.frequency = 60
		self.home_x_y()

	# ==========================================================================================
	# Control the servo connected to channel 14 of the servo control board to make the camera 
	# turning towards the positive direction of the x axis.
	# ==========================================================================================
	def move_decrease_x(self):
		self.Current_x += self.pas
		print(self.Current_x)
		if self.Current_x > self.Xmax:
			self.Current_x = self.Xmax
		self.pwm.write(14, 0, self.Current_x)   # CH14 <---> X axis
	# ==========================================================================================
	# Control the servo connected to channel 14 of the servo control board to make the camera 
	# turning towards the negative direction of the x axis.
	# ==========================================================================================
	def move_increase_x(self):
		self.Current_x -= self.pas
		print(self.Current_x)
		if self.Current_x <= self.Xmin:
			self.Current_x = self.Xmin
		self.pwm.write(14, 0, self.Current_x)
	# ==========================================================================================
	# Control the servo connected to channel 15 of the servo control board to make the camera 
	# turning towards the positive direction of the y axis. 
	# ==========================================================================================
	def move_increase_y(self):
		self.Current_y += self.pas
		print(self.Current_y)
		if self.Current_y > self.Ymax:
			self.Current_y = self.Ymax
		self.pwm.write(15, 0, self.Current_y)   # CH15 <---> Y axis
	# ==========================================================================================
	# Control the servo connected to channel 15 of the servo control board to make the camera 
	# turning towards the negative direction of the y axis. 
	# ==========================================================================================		
	def move_decrease_y(self):
		self.Current_y -= self.pas
		print(self.Current_y)
		if self.Current_y <= self.Ymin:
			self.Current_y = self.Ymin
		self.pwm.write(15, 0, self.Current_y)
	# ==========================================================================================		
	# Control the servos connected with channel 14 and 15 at the same time to make the camera 
	# move forward.
	# ==========================================================================================
	def home_x_y(self):
		self.Current_y = self.home_y 
		self.Current_x = self.home_x
		print(self.Current_x)
		self.pwm.write(14, 0, self.Current_x)
		self.pwm.write(15, 0, self.Current_y)

	def calibrate(self, x,y):
		self.pwm.write(14, 0, (self.MaxPulse+self.MinPulse)/2+x)
		self.pwm.write(15, 0, (self.MaxPulse+self.MinPulse)/2+y)