#!/usr/bin/env python3
# coding: utf-8	
import DistanceSensor as ds
import RPi.GPIO as GPIO
def main():
	print("salut")
	dSens = ds.DistanceSensor(25,24)
	print(" Trig "+str(dSens.Trig))
	print("Echo "+str(dSens.Echo))
	print(dSens.getDistance())
	dSens.cleanup()

if __name__ =='__main__':
	main()