#!/usr/bin/python

import sys
import sqlite3
import datetime
import calendar

INSERT_CHECKIN_EXPR = "INSERT INTO checkins VALUES(NULL,?,?,?,?);"
INSERT_PHOTO_EXPR = "INSERT INTO photos VALUES(NULL,?,?,?,?);"
INSERT_COMMENT_EXPR = "INSERT INTO comments VALUES(NULL,?,?,?);"
INSERT_TRAVEL_PARTY_EXPR = "INSERT INTO travel_parties VALUES(?,?);"

def saveMyPlace(uid, date_time, pic_url_str, comment, travel_party_str, perm, place_id_str):
    # process date_time
    date_time = calendar.timegm(datetime.datetime.now().timetuple()) # TODO: not use 'now'
    # process perm
    if perm == "Your Travel Party":
        perm = 1
    else:
        perm = 0
    # process place_id
    idx = place_id_str.rfind("-")
    place_id = place_id_str[idx+1]
    # process pic_url
    pic_urls = pic_url_str.split(',')
    # process travel_party
    travel_party_strs = travel_party_str.split(',')
    travel_party = []
    for tstr in travel_party_strs:
        idx = tstr.rfind("-")
        if idx != -1:
            travel_party.append(tstr[idx+1])
        

    # start inserting
    conn = sqlite3.connect('traceshare_test.db')
    c = conn.cursor()

    # insert checkins
    c.execute(INSERT_CHECKIN_EXPR, (date_time, place_id, uid, perm))
    cid = c.lastrowid
    print date_time, place_id, uid, perm, cid
    # insert photos
    for pic_url in pic_urls:
        print pic_url
        c.execute(INSERT_PHOTO_EXPR, (pic_url, uid, cid, place_id))
    # insert comment
    print comment
    c.execute(INSERT_COMMENT_EXPR, (uid, comment, cid))
    # insert travel_party
    for tid in travel_party:
        if tid != uid:
            print tid
            c.execute(INSERT_TRAVEL_PARTY_EXPR, (cid, tid))

    # commit to database
    conn.commit()
    conn.close()

    return cid

if __name__ == "__main__":
    saveMyPlace("1", "", "http://media-cdn.tripadvisor.com/media/photo-s/05/a6/f2/99/pier-39.jpg,http://media-cdn.tripadvisor.com/media/photo-s/05/a6/f0/f7/the-boys.jpg", "test comment", "travelparty-1, travelparty-2", "Your Travel Party", "place-1")
    #saveMyPlace("1", "", "http://media-cdn.tripadvisor.com/media/photo-s/05/a6/f2/99/pier-39.jpg", "test comment", "travelparty-1,travelparty-2,travelparty-3", "Your Travel Party", "place-1")
