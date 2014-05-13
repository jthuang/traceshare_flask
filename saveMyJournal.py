#!/usr/bin/python

import sys
import sqlite3
import datetime
import calendar

INSERT_JOURNAL_EXPR = "INSERT INTO journals VALUES(NULL,?,?,?,?,?);"
INSERT_JOURNAL_CHECKINS_EXPR = "INSERT INTO journal_checkins VALUES(?,?)"

def saveMyJournal(uid, date_time, title, desp, perm, cid_str):
    # process date_time
    date_time = calendar.timegm(datetime.datetime.now().timetuple())
    # process perm
    perm = 0
    if perm == "Your Travel Party":
        perm = 1

    # process cid
    cstrs = cid_str.split(',')
    cids = []
    for cstr in cstrs:
        idx = cstr.rfind("-")
        cids.append(cstr[idx+1])

    print date_time
    print perm
    print cids
        

    # start inserting
    conn = sqlite3.connect('traceshare_test.db')
    c = conn.cursor()

    # insert journal
    c.execute(INSERT_JOURNAL_EXPR, (date_time, title, desp, perm, uid))
    jid = c.lastrowid
    # insert journal_checkins
    for cid in cids:
        c.execute(INSERT_JOURNAL_CHECKINS_EXPR, (jid, cid))

    # commit to database
    conn.commit()
    conn.close()

    return jid

if __name__ == "__main__":
    saveMyJournal("1", "", "test title", "test desp", "Public", "cid-4,cid-3")
