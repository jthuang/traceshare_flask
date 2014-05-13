#!/usr/bin/python

import sys
import sqlite3

DEL_JOURNAL_EXPR = "DELETE FROM journals WHERE ((uid=?) and (jid=?));"
DEL_JOURNAL_CHECKIN_EXPR = "DELETE FROM journal_checkins WHERE (jid=?);"

def delMyJournal(uid, jid):
	conn = sqlite3.connect('traceshare_test.db')
	c = conn.cursor()
	c.execute(DEL_JOURNAL_EXPR, (uid,jid))
	c.execute(DEL_JOURNAL_CHECKIN_EXPR, (jid,))
	conn.commit()
	conn.close()
	return

if __name__ == "__main__":
	if len(sys.argv) != 3:
	    print "please enter the 'uid', 'jid'."
	else:
	    delMyJournal(sys.argv[1], sys.argv[2])
