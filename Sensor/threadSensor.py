#!/usr/bin/env python3
# coding: utf-8	
import DistanceSensor as ds
import RPi.GPIO as GPIO
def main():
	dSens = ds.DistanceSensor(16,18,GPIO.BCM)
	try:
		while(1):
			print(dSens.mesuring())
	except KeyboardInterrupt:
		print(" Exiting program")
	except:
		print(" Other exception detected")
	finally:
		dSens.cleanup()

if __name__ =='__main__':
	main()