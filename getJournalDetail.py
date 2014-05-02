#!/usr/bin/python

import sys
import sqlite3
import datetime

GET_JOURNAL_INFO_EXPR = "SELECT jid, time, name, desp, perm, uid FROM journals WHERE (jid = ?) ORDER BY time DESC;"
GET_JOURNAL_CHECKINS_EXPR = "SELECT cid FROM journal_checkins WHERE (jid = ?) ORDER BY cid ASC;"
GET_CHECKIN_INFO_EXPR = "SELECT time, place_id, host_uid, perm FROM checkins WHERE (cid = ?);"
GET_PLACE_NAME_LAT_LONG_EXPR = "SELECT name, lat, long FROM places WHERE (place_id = ?);"
GET_CHECKIN_PHOTO_URLS_EXPR = "SELECT photo_url FROM photos WHERE (cid = ?);"

# input  : jid
# output : journal_info{}
def getJournalDetail(jid):
   journal_info = {}
   
   conn = sqlite3.connect('traceshare_test.db')
   c = conn.cursor()

   # get jid, time, name, desp, perm, uid of the journal
   c.execute(GET_JOURNAL_INFO_EXPR, (jid,))
   j = c.fetchone()
   if j == None:
      conn.close()
      return journal_info
   
   journal_info['jid'] = j[0]
   journal_info['time'] = datetime.datetime.fromtimestamp(int(j[1])).strftime('%Y-%m-%d %H:%M:%S')
   journal_info['name'] = j[2]
   journal_info['desp'] = j[3]
   journal_info['perm'] = j[4]
   journal_info['uid'] = j[5]
   journal_info['checkins'] = []
   
   # get cids in journal
   for cid in c.execute(GET_JOURNAL_CHECKINS_EXPR, (journal_info['jid'],)):
      checkin = {}
      checkin['cid'] = cid[0]
      journal_info['checkins'].append(checkin)

   # checkin info in cids
   for checkin in journal_info['checkins']:
      c.execute(GET_CHECKIN_INFO_EXPR, (str(checkin['cid']),))
      cinfo = c.fetchone()
      if cinfo == None:
         continue
      
      checkin['time'] = datetime.datetime.fromtimestamp(int(cinfo[0])).strftime('%Y-%m-%d %H:%M:%S')
      checkin['place_id'] = cinfo[1]
      checkin['host_uid'] = cinfo[2]
      checkin['perm'] = cinfo[3]

      # get place name, lat, long
      c.execute(GET_PLACE_NAME_LAT_LONG_EXPR, str(checkin['place_id']))
      (checkin['name'], checkin['lat'], checkin['long']) = c.fetchone()

      # get place photo_url
      photo_urls = []
      for photo_url in c.execute(GET_CHECKIN_PHOTO_URLS_EXPR, (checkin['cid'],)):
         photo_urls.append(photo_url[0])
      checkin['photo_urls'] = photo_urls

   conn.close()
   return journal_info


def printJournalInfo(journal_info):
   print journal_info
   print "======================================================"
   
   print "time:",  journal_info['time']
   print "name:",  journal_info['name']
   print "desp:",  journal_info['desp']
   print "uid:",  journal_info['uid']
   print "perm:",  journal_info['perm']

   print "======================================================"
   print "checkins:"
   for checkin in journal_info['checkins']:
      print "\tcid:", checkin['cid']
      print "\ttime:", checkin['time']
      print "\tplace_id:", checkin['place_id']
      print "\thost_uid:", checkin['host_uid']
      print "\tperm:", checkin['perm']
      print "\tname:", checkin['name']
      print "\tlat, long:", checkin['lat'], checkin['long']
      
      print "\tphotos:"
      for photo_url in checkin['photo_urls']:
         print "\t\tcid:", photo_url

      print "======================================================"


if __name__ == "__main__":
   if len(sys.argv) != 2:
      print "please enter the 'jid'."
   else:
      journal_info = getJournalDetail(sys.argv[1])
      printJournalInfo(journal_info)
