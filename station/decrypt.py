#!/usr/bin/python3
#-*- coding: utf-8 -*-

class Coord():
	#########################################
	# Initialise le fichier à lire et les
	# attributs latitude, longitude.
	# file_name : le fichier contenant les
	# coordonnées gps.
	#########################################
	def __init__(self, file_name):
		self._file_name = file_name
		self._latitude = 0
		self._longitude = 0
	##########################################
	# stocke la latitude et la longitude de la
	# dernière ligne du fichier contenant la 
	# position gps.
	##########################################
	def get_last_position(self):
		f = open(self._file_name, "r")
		line_list = f.readlines()
		f.close()
		print(line_list)
		splited_line = (line_list[len(line_list)-1]).split(',')
		self._latitude = splited_line[1]
		self._longitude = splited_line[3]
		print("latitude", self._latitude, "longitude", self._longitude)

def main():
	c = Coord("coord.txt")
	c.get_last_position()

if __name__ == '__main__':
	main()