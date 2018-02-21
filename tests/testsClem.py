#!/usr/bin/env python
import sys
sys.path.insert(0, '../actuators/')
sys.path.insert(0, '../sensors/')

from CarDirection import CarDirection
from VideoDirection import VideoDirection
from Motor import Motor
from WheelSensor import WheelSensor
from DistanceSensor import DistanceSensor

import time                # Import necessary modules

def test_burn(motor, car_dir):
	car_dir.turn_right()
	motor.burn()
	time.sleep(10)
	motor.stop()

def test_forward(motor, car_dir, t):
	car_dir.home()
	motor.forward()
	time.sleep(t)
	motor.stop()

def test_forward_for(motor, car_dir, wheel_sensor, distance):
	car_dir.home()
	motor.forward()
	wheel_sensor.wait_for(distance)
	motor.stop()

if __name__ == '__main__':
	# motor = Motor()
	# car_dir = CarDirection()
	# vid_dir = VideoDirection()
	# # wheel_sensor = WheelSensor()
	# # distance_sensor = DistanceSensor()

	# motor.setSpeed(100)

	# # test_burn(motor, car_dir)
	# # test_forward(motor, car_dir, 10)

	# # car_dir.turn(90)
	# # vid_dir.move_decrease_x()
	# vid_dir.home_x_y()
	# # vid_dir.move_increase_y()

	file = open("tasoeur.txt", 'wb')
	file.write(b'123')
	file.close()