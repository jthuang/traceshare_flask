#!/usr/bin/python

import sys
import sqlite3
import datetime
from getRecommendedPlaces import getRecommendedPlaces 

GET_PUBLIC_CHECKINS_PID_EXPR = "SELECT cid FROM checkins WHERE ((place_id = ?) AND (perm = 0));"
GET_CHECKIN_INFO_CID_EXPR = "SELECT cid, time, place_id FROM checkins WHERE (cid = ?);"
GET_ONE_PHOTO_URL_EXPR = "SELECT photo_url FROM photos WHERE (cid = ?) LIMIT 1;"
GET_PLACE_NAME_LAT_LONG_EXPR = "SELECT name, lat, long FROM places WHERE (place_id = ?);"

# input  : uid, geo_info
# output : places[{}]
def getExploredPlaces(uid, geo_info):
	places = []
	# get recommended place_ids
	place_ids = getRecommendedPlaces(uid, geo_info)

	conn = sqlite3.connect('traceshare_test.db')
	c = conn.cursor()

	# get public checkins with thoes place_ids (get cid, time)
	checkin_set = set()
        for pid in place_ids:
		for cid in c.execute(GET_PUBLIC_CHECKINS_PID_EXPR, (str(pid),)):
		    checkin_set.add(cid[0])

        for cid in checkin_set:
		place_info = {}
		c.execute(GET_CHECKIN_INFO_CID_EXPR, (str(cid),))
		p = c.fetchone()
		place_info['cid'] = p[0]
		place_info['time'] = datetime.datetime.fromtimestamp(int(p[1])).strftime('%Y-%m-%d %H:%M:%S')
		place_info['place_id'] = p[2]
		places.append(place_info)

	# get place info
	for p in places:
		# get photo_url
		c.execute(GET_ONE_PHOTO_URL_EXPR, (str(p['cid']),))
		p['photo_url'] = c.fetchone()[0]
		
		# get place name, lat, long
		c.execute(GET_PLACE_NAME_LAT_LONG_EXPR, (str(p['place_id'],)))
		(p['place_name'], p['lat'], p['long']) = c.fetchone()

	conn.close()

	return places



def printExploredPlaces(places):
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
		places = getExploredPlaces(sys.argv[1], [])
		printExploredPlaces(places)
