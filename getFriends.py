#!/usr/bin/python

import sys
import sqlite3

GET_FRIENDS_EXPR = "SELECT uid2 FROM friendship WHERE (uid1 = ?);"
GET_USER_EXPR = "SELECT name, pic_url FROM users WHERE (uid = ?);"

# input  : uid
# output : friends
def getFriends(uid):
	friends = []
	fuids = []

	conn = sqlite3.connect('traceshare_test.db')
	c = conn.cursor()

	# get friend uid
	for f in c.execute(GET_FRIENDS_EXPR, (uid,)):
		fuids.append(f[0])

	# get friend name, pic_url
	for uid in fuids:
		friend = {}
		friend['uid'] = uid
		c.execute(GET_USER_EXPR, (str(uid),))
		(friend['name'], friend['pic_url']) = c.fetchone()
		friends.append(friend)


	conn.close()

	return friends


def printFriends(friends):
	print friends
	print "======================================================"
	for f in friends:
		print f['uid'], f['name'], f['pic_url']

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print "please enter the 'uid'."
	else:
		friends = getFriends(sys.argv[1])
		printFriends(friends)
