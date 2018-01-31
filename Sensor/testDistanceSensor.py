#!/usr/bin/env python3
# coding: utf-8	
import DistanceSensor as ds
import RPi.GPIO as GPIO
def main():
	
	try:
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(12, GPIO.OUT)
		p=GPIO.PWM(12, 20)

		p.start(1)
	except KeyboardInterrupt:
		print(" Exiting program")
	except:
		print(" Other exception detected\n"+str(sys.exc_info()[0]) )
	finally:
		GPIO.cleanup()

	"""dSens = ds.DistanceSensor(16,18,GPIO.BCM)
	print(" Trig "+str(dSens.Trig))
	print(" Echo "+str(dSens.Echo))
	print(dSens.getDistance())"""


	"""while(1):
		machin = raw_input(" Voulez vous une mesure -> 1 : ")
		if machin == '1' :
			print(" Mesuring ...")
			dSens.trigerMesure()

	dSens.cleanup()"""

if __name__ =='__main__':
	main()