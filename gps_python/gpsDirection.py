#!/usr/bin python3
# coding: utf-8	

import math

def toRad(degrees):
	return degrees*(math.pi/180)

def toDegrees(radians):
	return radians*180/math.pi

def toBearing(radians):
	return (toDegrees(radians)+360)%360

def DegreeBearing(lat1, lon1, lat2, lon2):
	dLon = toRad(lon2-lon1)
	dPhi = math.log(math.tan(toRad(lat2)/2+math.pi/4)/math.tan(toRad(lat1)/2+math.pi/4))
	if (math.fabs(dLon)>math.pi):
		dLon=-(2*math.pi-dLon) if dLon>0 else (2*math.pi+dLon)
	return toBearing(math.atan2(dLon,dPhi))

from math import radians, cos, sin, asin, sqrt
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km*1000


def DmsToDD(degrees, minutes, secondes):
	if degrees > 0:
		return ((float(secondes)/3600) + (float(minutes)/60) + float(degrees))
	else:
		return (-(float(secondes)/3600) - (float(minutes)/60) + float(degrees))

def DmToDD(degrees, minutes):
	return DmsToDD(degrees, int(minutes), (minutes-int(minutes))*60)

def castMStoM(minutes, secondes):
	return minutes+secondes/60


def main():
	print(" A que coucou !")
	print(DegreeBearing(43.561206,1.466015,43.561068,1.465776))
	print(haversine(1.465776, 43.561068, 1.466015, 43.561206))

	print(DmsToDD(43,33,39.845))
	print(DmsToDD(1,27,56.793))
		
	print(DmToDD(43,33+39.845/60))
	print(DmToDD(1,27+56.793/60))

	print(DmToDD(43,castMStoM(33, 39.845)))
	print(DmToDD(1,castMStoM(27, 56.793)))
if __name__ =='__main__':
	main(	)