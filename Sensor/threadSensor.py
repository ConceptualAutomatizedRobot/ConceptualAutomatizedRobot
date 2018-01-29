#!/usr/bin/env python3
# coding: utf-8	
import DistanceSensor as ds
import RPi.GPIO as GPIO
def main():
	dSens = ds.DistanceSensor(25,24,GPIO.BCM)
	while(1):
		print(dSens.mesuring())

	dSens.cleanup()

if __name__ =='__main__':
	main()