#!/usr/bin/python

import sys
import sqlite3

DEL_JOURNAL_EXPR = "DELETE FROM journals WHERE ((uid=?) and (jid=?));"
DEL_JOURNAL_CHECKIN_EXPR = "DELETE FROM journal_checkins WHERE (jid=?);"
DEL_TMP_CHECKINS_EXPR = "DELETE FROM checkins WHERE (cid=?);"

def delMyJournal(uid, jid, tmp_cid_str):
    cids = []
    # process tmp_cid
    cstrs = tmp_cid_str.split(',')
    for cstr in cstrs:
        idx = cstr.rfind("-")
        if idx != -1:
            cids.append(cstr[idx+1])
    print cids
            
    conn = sqlite3.connect('traceshare_test.db')
    c = conn.cursor()
    c.execute(DEL_JOURNAL_EXPR, (uid,jid))
    c.execute(DEL_JOURNAL_CHECKIN_EXPR, (jid,))
    for cid in cids:
        c.execute(DEL_TMP_CHECKINS_EXPR, (cid,))

    conn.commit()
    conn.close()
    
    return

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "please enter the 'uid', 'jid', 'cids'."
    else:
        delMyJournal(sys.argv[1], sys.argv[2], sys.argv[3])
