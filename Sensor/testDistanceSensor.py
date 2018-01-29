#!/usr/bin/env python3
# coding: utf-8	
import DistanceSensor as ds
import RPi.GPIO as GPIO
def main():
	dSens = ds.DistanceSensor(25,24,GPIO.BCM)
	print(" Trig "+str(dSens.Trig))
	print(" Echo "+str(dSens.Echo))
	print(dSens.getDistance())

	while(1):
		machin = raw_input(" Voulez vous une mesure -> 1 : ")
		if machin == '1' :
			print(dSens.trigerMesure())

	dSens.cleanup()

if __name__ =='__main__':
	main()