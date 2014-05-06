#!/usr/bin/python

import sys
import sqlite3

GET_USER_EXPR = "SELECT uid, name, pic_url FROM users WHERE (uid = ?);"

# input  : uid
# output : user_info
def getUser(uid):
	user = {}

	conn = sqlite3.connect('traceshare_test.db')
	c = conn.cursor()

	# get user info
	c.execute(GET_USER_EXPR, (str(uid),))
	(user['uid'], user['name'], user['pic_url']) = c.fetchone()

	conn.close()

	return user


def printUser(user):
	print user
	print "======================================================"
	print user['uid'], user['name'], user['pic_url']

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print "please enter the 'uid'."
	else:
		user = getUser(sys.argv[1])
		printUser(user)
