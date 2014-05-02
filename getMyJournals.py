#!/usr/bin/python

import sys
import sqlite3
import datetime

GET_JOURNALS_EXPR = "SELECT jid, time, name, desp, perm, uid FROM journals WHERE (uid = ?) ORDER BY time DESC;"
GET_JOURNAL_CHECKINS_EXPR = "SELECT cid FROM journal_checkins WHERE (jid = ?) ORDER BY cid ASC;"
GET_CHECKIN_PLACEID_EXPR = "SELECT place_id FROM checkins WHERE (cid = ?);"
GET_CHECKIN_LAT_LONG_EXPR = "SELECT lat, long FROM places WHERE (place_id = ?);"

# input  : uid
# output : journals[{}]
def getMyJournals(uid):
   journals = []
   
   conn = sqlite3.connect('traceshare_test.db')
   c = conn.cursor()

   # get jid, time, name, desp, perm, uid of journals
   for j in c.execute(GET_JOURNALS_EXPR, (uid,)):
      journal_info = {}
      journal_info['jid'] = j[0]
      journal_info['time'] = datetime.datetime.fromtimestamp(int(j[1])).strftime('%Y-%m-%d %H:%M:%S')
      journal_info['name'] = j[2]
      journal_info['desp'] = j[3]
      journal_info['perm'] = j[4]
      journal_info['uid'] = j[5]
      journals.append(journal_info)

   # get checkins in journal
   for journal_info in journals:
      journal_info['checkins'] = []
      for cid in c.execute(GET_JOURNAL_CHECKINS_EXPR, (journal_info['jid'],)):
         checkin = {}
         checkin['cid'] = cid[0]
         journal_info['checkins'].append(checkin)

   # get place_id, "at, long of the checkins
   for journal_info in journals:
      for checkin in journal_info['checkins']:
         # get place_id
         c.execute(GET_CHECKIN_PLACEID_EXPR, (str(checkin['cid']),))
         checkin['place_id'] = c.fetchone()[0]
         # get lat, long
         c.execute(GET_CHECKIN_LAT_LONG_EXPR, (str(checkin['place_id']),))
         (checkin['lat'], checkin['long']) = c.fetchone()

   conn.close()
   return journals


def printMyJournals(journals):
   print journals
   for j in journals:
      print "======================================================"
      print "jid:", j['jid']
      print "time:", j['time']
      print "name:", j['name']
      print "desp:", j['desp']
      print "perm:", j['perm']
      print "uid:", j['uid']
      
      print "checkins:"
      for c in j['checkins']:
         print "\t", c['cid'], c['place_id'], c['lat'], c['long']

if __name__ == "__main__":
   if len(sys.argv) != 2:
      print "please enter the 'uid'."
   else:
      journals = getMyJournals(sys.argv[1])
      printMyJournals(journals)
