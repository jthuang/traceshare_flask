#!/usr/bin/python

import sys
import sqlite3
import datetime

GET_PLACES_EXPR = "SELECT cid, time, place_id FROM checkins WHERE (host_uid = ?) ORDER BY time DESC;"
GET_ONE_PHOTO_URL_EXPR = "SELECT photo_url FROM photos WHERE (cid = ?) LIMIT 1;"
GET_PLACE_NAME_LAT_LONG_EXPR = "SELECT name, lat, long FROM places WHERE (place_id = ?);"

# input  : cid
# output : places[{}]
def getMyPlaces(uid):
	places = []

	conn = sqlite3.connect('traceshare_test.db')
	c = conn.cursor()

	# get cid, time, place_id
	for p in c.execute(GET_PLACES_EXPR, uid):
		place_info = {}
		place_info['cid'] = p[0]
		place_info['time'] = datetime.datetime.fromtimestamp(int(p[1])).strftime('%Y-%m-%d %H:%M:%S')
		place_info['place_id'] = p[2]
		places.append(place_info)

	# get photo_url
	for p in places:
		# get photo_url
		c.execute(GET_ONE_PHOTO_URL_EXPR, str(p['cid']))
		p['photo_url'] = c.fetchone()[0]
		
		# get place name, lat, long
		c.execute(GET_PLACE_NAME_LAT_LONG_EXPR, str(p['place_id']))
		(p['place_name'], p['lat'], p['long']) = c.fetchone()
	
	conn.close()

	return places


def printMyPlaces(places):
	print places
	for p in places:
		print "======================================================"
		print "cid:", p['cid']
		print "time:", p['time']
		print "place_id:", p['place_id']
		print "place_name:", p['place_name']
		print "lat:", p['lat']
		print "long:", p['long']
		print "photo_url:", p['photo_url']


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print "please enter the 'uid'."
	else:
		places = getMyPlaces(sys.argv[1])
		printMyPlaces(places)
