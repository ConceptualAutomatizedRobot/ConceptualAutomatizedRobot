#!/usr/bin/python
#-*- coding: utf-8 -*-

from system import System
import time

import sys
sys.path.insert(0,"../sensors/")
from DistanceSensor import DistanceSensor
from WheelSensor import WheelSensor


if __name__ == "__main__":
	Sys = System()
	# DS = DistanceSensor(Sys)
	# WS = WheelSensor(Sys)

	Sys.start()
	# DS.start()
	# WS.start()

	# Sys.notify({"type":System.E_POS,"value":0})
	# time.sleep(2)

	# Sys.notify({"type":System.E_POS,"value":1})
	# time.sleep(0.2)

	# Sys.notify({"type":System.E_POS,"value":0})
	# time.sleep(0.5)

	# Sys.notify({"type":System.E_POS,"value":-1})
	# time.sleep(0.4)

	# Sys.notify({"type":System.E_POS,"value":0})
	# time.sleep(2)


	Sys.stop()
	# DS.stop()
	# WS.stop()

	Sys.join()
	# DS.join()
	# WS.join()
