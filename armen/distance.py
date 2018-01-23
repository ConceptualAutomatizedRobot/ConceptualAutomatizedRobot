#!/usr/bin/env python

import motor as motor
import car_dir as dir
import time

if __name__ == '__main__':
	dir.setup()
	motor.setup()

	
	for x in xrange(1,5):
		dir.home()
		time.sleep(0.5)
		dir.turn_right()
		time.sleep(0.5)
		dir.turn_left()
		time.sleep(0.5)
	#motor.setSpeed(50)
	#motor.forward()
	time.sleep(2)
	motor.stop()