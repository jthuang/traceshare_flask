#!/usr/bin/python

import sys
import sqlite3

QUERY_PLACE_EXPR = "SELECT * FROM places WHERE (name=?);"
INSERT_PLACE_EXPR = "INSERT INTO places VALUES(NULL,?,?,?);"

def updatePlaceDB(name, lat, lng):
    conn = sqlite3.connect('traceshare_test.db')
    c = conn.cursor()

    c.execute(QUERY_PLACE_EXPR, (name,))
    place = c.fetchone()
    if place == None:
        c.execute(INSERT_PLACE_EXPR, (name, lat, lng))
        place_id = c.lastrowid
        conn.commit()
        print "Insert!", place_id
    else:
        place_id = place[0]
        print "Exist!", place_id

    conn.close()

    return place_id

if __name__ == "__main__":
    updatePlaceDB("test", "123", "456")



