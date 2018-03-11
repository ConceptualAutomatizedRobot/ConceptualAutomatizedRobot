#!/usr/bin/python3
#-*- coding: utf-8 -*-

import Coord
import Motor

class Path():
	def __init__(self, latitude_goal, longitude_goal, error_margin):
		self._latitude = latitude_goal
		self._longitude = longitude_goal
		self._error_margin = error_margin
	
	def go_to_the_area(self):
		tourner = 0
		arrived = 0
		c = Coord("coord.txt")
		m = Motor()
		while(not(arrived)):
			c.get_last_position()
			if c._latitude < ( self._latitude + self._error_margin):
				m.forward(10)
			elif c._latitude > ( self._latitude + self._error_margin):
				#demi tour
				m.left()
				m.backward(20,1)
				m.straigth_wheel()
			elif c._longitude < (self._longitude + self._error_margin):
				if tourner == 0:
					# tourner à droite
					m.right()
					m.forward(20,1)
					m.straigth_wheel()
					tourner == 1
				m.forward(10)
			elif c._longitude > (self._longitude + self._error_margin):
				if tourner == 0:
					#tourner à gauche
					m.left()
					m.forward(20,1)
					m.straigth_wheel()
					tourner == 1
				m.forward(10)
			#Si aucune condition n'est prise c'est que l'on est arrivé
			m.stop()
			arrived = 1

def main():
	p = Path(43.231, 12.45)
	p.go_to_the_area()

if __name__ == '__main__':
	main()