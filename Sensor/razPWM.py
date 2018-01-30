#!/usr/bin/env python3
# coding: utf-8	

import PCA9685 as servo
import sys
sys.path.insert(0, '../sunfounder/server')
sHori  = 14 # Servo moteur Camera Horizontale
sVerti = 15 # Servo moteur Camera Verticale
sRoue  = 0  # Servo moteur Roue
triger = 8  # Trigger du sonar

def setup():
	global pwmRAZ
	pwmRAZ = servo.PWM()

def raz():
	pwmRAZ.write(sHori, 0, 0)
	pwmRAZ.write(sVerti, 0, 0)
	pwmRAZ.write(sRoue, 0, 0)
	pwmRAZ.write(triger, 0, 0)


def main():
	raz()
	


if __name__ =='__main__':
	main()
