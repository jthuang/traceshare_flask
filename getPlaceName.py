#!/usr/bin/python

import sys
import sqlite3

GET_PLACE_BY_GEO_EXPR = "SELECT place_id, name, lat, long FROM places WHERE ()(lat = ?) and (long = ?));"

# input  : lat, lng
# output : place_info
def getPlaceInfoByGeo(lat, lng):
	place = {}

	conn = sqlite3.connect('traceshare_test.db')
	c = conn.cursor()

	# get friend uid
	for p in c.execute(GET_PLACE_BY_GEO_EXPR, (lat, lng)):
		place['place_id'] = p[0]
		place['name'] = p[1]
		place['lat'] = p[2]
		place['long'] = p[3]

	conn.close()

	return place


def printPlace(place):
	print place
	print "======================================================"
	print place['place_id'], place['name'], place['lat'], place['long']

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "please enter the 'lat' and 'long'."
    else:
        place = getPlaceInfo(argv[1], argv[2])
        printPlace(place)
