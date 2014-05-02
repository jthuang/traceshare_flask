#!/usr/bin/python

import sys
import sqlite3
import datetime

GET_PLACE_INFO_EXPR = "SELECT * FROM checkins WHERE (cid = ?);"
GET_TRAVEL_PARTIES_EXPR = "SELECT uid FROM travel_parties WHERE (cid = ?);"
GET_USER_EXPR = "SELECT name, pic_url FROM users WHERE (uid = ?);"
GET_PLACE_PHOTO_URLS_EXPR = "SELECT photo_url  FROM photos WHERE (cid = ?);"
GET_COMMENTS_EXPR = "SELECT comment_id, uid, comment_str FROM comments WHERE (cid = ?);"
GET_PLACE_NAME_LAT_LONG_EXPR = "SELECT name, lat, long FROM places WHERE (place_id = ?);"

# input  : cid
# output : place_info{}
def getPlaceDetail(cid):
	place_info = {}
	uids = []

	conn = sqlite3.connect('traceshare_test.db')
	c = conn.cursor()

	# get cid, time, place_id, host_uid, perm
	c.execute(GET_PLACE_INFO_EXPR, cid)
	p = c.fetchone()
        if p == None:
           conn.close()
           return place_info

	place_info['cid'] = p[0]
	place_info['time'] = datetime.datetime.fromtimestamp(int(p[1])).strftime('%Y-%m-%d %H:%M:%S')
	place_info['place_id'] = p[2]
	place_info['host_uid'] = p[3]
	place_info['perm'] = p[4]

	# push the host_uid as the first uid
	uids.append(place_info['host_uid'])

	# get other uids
	for u in c.execute(GET_TRAVEL_PARTIES_EXPR, cid):
		uids.append(u[0])

	# get pic_url of each user
	place_info['users'] = []
	for u in uids:
		user = {}
		user['uid'] = u
		c.execute(GET_USER_EXPR, str(u))
		(user['name'], user['pic_url']) = c.fetchone()
		place_info['users'].append(user)

	# get place photo_url
	photo_urls = []
	for photo_url in c.execute(GET_PLACE_PHOTO_URLS_EXPR, cid):
		photo_urls.append(photo_url[0])
	place_info['photo_urls'] = photo_urls

	# get comments
	comments = []
	for (comment_id, uid, comment_str) in c.execute(GET_COMMENTS_EXPR, cid):
		comment = {}
		comment['comment_id'] = comment_id
		comment['uid'] = uid
		comment['comment_str'] = comment_str
		comments.append(comment)
	place_info['comments'] = comments

	# get place lat, long
	c.execute(GET_PLACE_NAME_LAT_LONG_EXPR, str(place_info['place_id']))
	(place_info['name'], place_info['lat'], place_info['long']) = c.fetchone()

	conn.close()

	return place_info


def printPlaceInfo(place_info):
	print place_info
	print "======================================================"
	print "name:",  place_info['name']
	print "time:", place_info['time']
	print "photos:"
	for photo_url in place_info['photo_urls']:
		print "\t", photo_url
	print "perm:", place_info['perm']
	print "users:"
	for user in place_info['users']:
		print "\t", user['uid'], user['name'], user['pic_url']
	print "comments:"
	for comment in place_info['comments']:
		print "\t", comment['comment_id'], comment['uid'], comment['comment_str']
	print "lat, long:", place_info['lat'], ",", place_info['long']


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print "please enter the 'cid'."
	else:
		place_info = getPlaceDetail(sys.argv[1])
		printPlaceInfo(place_info)
