#!/usr/bin/python
#-*- coding: utf-8 -*-

from datetime import datetime
import os.path

class Logfile():

	_path = None

	###########################
	# Constructeur
	# path : Chemin du répertoire où sont stockées les logs
	###########################
	def __init__(self,path):
		self._path = path+"/log"+str(datetime.now().date())+"--"+str(datetime.now().time())
		open(self._path,"w").close()
	
	###########################
	# Destructeur
	###########################
	def __del__(self):
		file = open(self._path,"a")
		file.write("Fin de session :: "+str(datetime.now().date())+"--"+str(datetime.now().time()))
		file.close()

	###########################
	# Ecriture dans les logs
	# msg : message a écrire, enregistré sous la forme "date-heure :: msg"
	###########################
	def write(self,msg):
		file = open(self._path,"a")
		lm = str(datetime.now().date())+"--"+str(datetime.now().time())+" :: "+str(msg)
		print(lm)
		file.write(lm+'\n')
		file.close()

	###########################
	# Lecture
	# retourne le contenu du fichier de log courrant
	###########################
	def read(self):
		file = open(self.path,"r")
		r = file.read()
		file.close()

		return r

	###########################
	# Retourne le chemin du fichier log courrant
	##########################
	def get_path(self):
		return self._path


if __name__ =="__main__":
	path = "/nfs/home/camsi9/Documents/workspace/CAR"
	log = Logfile(path)

	logpath = log.get_path()
	assert os.path.isfile(logpath), logpath+" does not exist"

	log.write("Direction set : -45")
	log.write("Moteur set : 50")

	print(log.read())

	del log

	assert (not 'log' in vars()), "log not deleted"