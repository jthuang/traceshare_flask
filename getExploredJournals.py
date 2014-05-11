#!/usr/bin/python

import sys
import sqlite3
import datetime
from getRecommendedPlaces import getRecommendedPlaces 

GET_PUBLIC_CHECKINS_PID_EXPR = "SELECT cid FROM checkins WHERE ((place_id = ?) AND (perm = 0));"
GET_JOURNALS_FROM_CIDS_EXPR = "SELECT jid FROM journal_checkins where (cid = ?);"
GET_JOURNALS_EXPR = "SELECT jid, time, name, desp, perm, uid FROM journals WHERE ((jid = ?) AND (perm = 0)) ;"
GET_JOURNAL_CHECKINS_EXPR = "SELECT cid FROM journal_checkins WHERE (jid = ?) ORDER BY cid ASC;"
GET_CHECKIN_PLACEID_EXPR = "SELECT place_id FROM checkins WHERE (cid = ?);"
GET_CHECKIN_LAT_LONG_EXPR = "SELECT lat, long FROM places WHERE (place_id = ?);"

# input  : uid, geo_info
# output : journals[{}]
def getExploredJournals(uid, geo_info):
    journals = []
    
    # get recommended place_ids
    place_ids = getRecommendedPlaces(uid, geo_info)
    
    conn = sqlite3.connect('traceshare_test.db')
    c = conn.cursor()
    
    # get public checkins with thoes place_ids
    checkin_set = set()
    for pid in place_ids:
        for cid in c.execute(GET_PUBLIC_CHECKINS_PID_EXPR, (str(pid),)):
            checkin_set.add(cid[0])

    # get public journa_ids with thoes place_ids
    jid_set = set()
    for cid in checkin_set:
        for j in c.execute(GET_JOURNALS_FROM_CIDS_EXPR, (str(cid),)):
            jid_set.add(j[0])


    # get public journals with thoes place_ids (get jid, time, name, desp, perm, uid)
    for jid in jid_set:
        for j in c.execute(GET_JOURNALS_EXPR, (jid,)):
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

    # get place_id, lat, long of the checkins
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



def getRecommendedPlaces(uid, geo_info):
	return [1, 2]
#	conn = sqlite3.connect('traceshare_test.db')
#	c = conn.cursor()

#	my_places = 
#	conn.close()

def printExploredJournals(journals):
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
        journals = getExploredJournals(sys.argv[1], [])
        printExploredJournals(journals)
