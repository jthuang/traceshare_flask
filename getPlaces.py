#!/usr/bin/python

import sys
import sqlite3

GET_PLACES_EXPR = "SELECT place_id, name, lat, long FROM places;"

# input  : 
# output : places
def getPlaces():
	places = []

	conn = sqlite3.connect('traceshare_test.db')
	c = conn.cursor()

	# get friend uid
	for p in c.execute(GET_PLACES_EXPR):
		place = {}
		place['place_id'] = p[0]
		place['name'] = p[1]
		place['lat'] = p[2]
		place['long'] = p[3]
		places.append(place)

	conn.close()

	return places


def printPlaces(places):
	print places
	print "======================================================"
	for p in places:
		print p['place_id'], p['name'], p['lat'], p['long']

if __name__ == "__main__":
		places = getPlaces()
		printPlaces(places)
