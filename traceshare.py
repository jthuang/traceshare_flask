import flask
from flask import request
from os import environ
from getMyPlaces import getMyPlaces
from getMyJournals import getMyJournals
from getPlaceDetail import getPlaceDetail
from getJournalDetail import getJournalDetail

app = flask.Flask(__name__)

# log to stderr
import logging
from logging import StreamHandler
file_handler = StreamHandler()
app.logger.setLevel(logging.DEBUG)  # set the desired logging level here
app.logger.addHandler(file_handler)

@app.route('/')
def hello():
    return 'Hello World! TraceShare!'

@app.route('/mytrace', methods=["GET"])
def get_my_trace():
   uid = request.args.get('uid', "1")
   app.logger.debug("Accessing mytrace.html", uid)
   
   places = getMyPlaces(uid)
   journals = getMyJournals(uid)

   resp = flask.make_response(flask.render_template(
            'mytrace.html',
            places=places,
            journals=journals))
   return resp

@app.route('/placemap', methods=["GET"])
def get_my_place_map():
   uid = request.args.get('uid', "1")
   app.logger.debug("Accessing placemap.html", uid)
   
   places = getMyPlaces(uid)

   resp = flask.make_response(flask.render_template(
            'placemap.html',
            places=places))
   return resp

@app.route('/placedetail', methods=["GET"])
def get_place_detal():
   cid = request.args.get('cid', "1")
   app.logger.debug("Accessing placedetail.html", cid)
   
   place_info = getPlaceDetail(cid)

   resp = flask.make_response(flask.render_template(
            'placedetail.html',
            place_info=place_info))
   return resp

@app.route('/journaldetail', methods=["GET"])
def get_journal_detal():
   jid = request.args.get('jid', "1")
   app.logger.debug("Accessing journaldetail.html", jid)
   
   journal_info = getJournalDetail(jid)

   resp = flask.make_response(flask.render_template(
            'journaldetail.html',
            journal_info=journal_info))
   return resp

@app.route('/placeEdit', methods=["GET"])
def edit_my_place():
    app.logger.debug("Accessing placeEdit.html")
    resp = flask.make_response(flask.render_template('placeEdit.html'))
    return resp

@app.route('/placeUpdate', methods=["POST"])
def update_my_place():
    app.logger.debug("Accessing placeUpdate")
    place_id = request.form.get('placeId', "")
    date_time = request.form.get('dateTime', "")
    share_option = request.form.get('shareOption', "")
    string = place_id + " " + date_time + " " + share_option
    return place_id

#    resp = flask.make_response(flask.render_template('placeEdit.html'))
#    return resp

if __name__ == "__main__":
   #get_my_trace()
   app.run()
