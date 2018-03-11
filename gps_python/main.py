#!/usr/bin/env python3
# coding: utf-8

import gps
import gpsDirection as gpsD
import motor_nico as mn
import time

def main():
	print("Affichage de la distance à la destination et les longitudes.")

	myGps = gps.Gps()
	myGps.read_next()
	myGps.read_next()


	print(myGps.longitude())
	print(myGps.latitude())
	
	longDest = 1.465776
	latDest = 43.561068

	lastLong = myGps.longitude()
	lastLat = myGps.latitude()


	myMotor = mn.Motor()
	lastLongDD = gpsD.DmToDD(lastLong[0],lastLong[1])
	lastLatDD = gpsD.DmToDD(lastLat[0], lastLat[1])


	lastLatDD_minus1 = lastLatDD
	lastLongDD_minus1 = lastLongDD

	while ( gpsD.haversine(lastLongDD, lastLatDD, longDest, latDest)  > 5):

		distance = gpsD.haversine(lastLongDD, lastLatDD, longDest, latDest)
		print('########################################################')
		print('# Distance à la destination: '+ str(distance) + ' métres')
		print('# Longitude actuelle: '+ str(lastLongDD)+ ' Latitude actuelle: '+ str(lastLatDD)+ '\n#	 Longitude destination: '+ str(longDest)+ ' Latitude destination: '+ str(latDest))
		print('########################################################')


		myMotor.forward(102)
		# Correction de la trajectoire
		orientationActuelle = gpsD.DegreeBearing(lastLatDD_minus1, lastLongDD_minus1, lastLatDD, lastLongDD)
		orientationNeeded = gpsD.DegreeBearing(lastLatDD, lastLongDD, latDest, longDest) 
		deltaToCorrect = (orientationNeeded+360-orientationActuelle)%360
		print("--------------------------------------------------------")
		print(" Orientation ACTUELLE : "+str(orientationActuelle))
		print(" Orientation Dont ON a besoin  : "+str(orientationNeeded))
		print(" Difference à Corriger "+str(deltaToCorrect))
		print("--------------------------------------------------------")

		angleDefaut=orientationActuelle-orientationNeeded
		if angleDefaut > 180:
			angleDefaut = angleDefaut-360
		elif angleDefaut < -180:
			angleDefaut = angleDefaut+360

		angleDeltaErreur = 10
		if angleDefaut > 0 and angleDefaut>angleDeltaErreur:
			#-tourner a gauche
			myMotor.left()
			time.sleep(0.5)
			pass
		elif angleDefaut < 0 and angleDefaut> -angleDeltaErreur:
			# Tourner a droite
			myMotor.right()
			time.sleep(0.5)
		else :
			myMotor.straigth_wheel()
			time.sleep(0.5)



		time.sleep(1)

		# Interogation du gps
		myGps.read_next()
		# Récupération de nouvelles coordonnées
		lastLong = myGps.longitude()
		lastLat = myGps.latitude()
		# Sauvegade des ancienne coordonnée pour connaitre ma direction à l'instant t
		lastLongDD_minus1 = lastLongDD
		lastLatDD_minus1 =lastLatDD
		# COnvertion en Degrées décimaux
		lastLongDD = gpsD.DmToDD(lastLong[0],lastLong[1])
		lastLatDD = gpsD.DmToDD(lastLat[0], lastLat[1])

	myMotor.stop()


	print(myGps.longitude())
	print(myGps.latitude())



if __name__ =='__main__':
	main(	)
