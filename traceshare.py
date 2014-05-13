import flask
from flask import request
from os import environ
from getMyPlaces import getMyPlaces
from getMyJournals import getMyJournals
from getPlaceDetail import getPlaceDetail
from getJournalDetail import getJournalDetail
from getFriends import getFriends
from getPlaces import getPlaces
from getUser import getUser
from uploadr import FlickrUpload, FlickrGetPlaceName
from getExploredPlaces import getExploredPlaces
from getExploredJournals import getExploredJournals
from saveMyPlace import saveMyPlace
from getPlaceByGeo import getPlaceByGeo
from saveMyJournal import saveMyJournal
from delMyJournal import delMyJournal
import datetime

app = flask.Flask(__name__)

# log to stderr in Heroku
import logging
from logging import StreamHandler
file_handler = StreamHandler()
app.logger.setLevel(logging.DEBUG)  # set the desired logging level here
app.logger.addHandler(file_handler)

@app.route('/')
def hello():
    return 'Hello World! <a href="/mytrace">TraceShare!</a>'

@app.route('/explore', methods=["GET"])
def get_explore():
   uid = request.args.get('uid', "1")
   app.logger.debug("Accessing explore.html %s", uid)
   geo_info = {}
   geo_info['lat'] = request.args.get('lat', "")
   geo_info['long'] = request.args.get('long', "")
   
   places = getExploredPlaces(uid, geo_info)
   journals = getExploredJournals(uid, geo_info)

   resp = flask.make_response(flask.render_template(
            'trace.html',
            places=places,
            journals=journals,
            option="explore"))
   return resp

@app.route('/mytrace', methods=["GET"])
def get_my_trace():
   uid = request.args.get('uid', "1")
   app.logger.debug("Accessing mytrace.html %s", uid)
   
   places = getMyPlaces(uid)
   journals = getMyJournals(uid)

   resp = flask.make_response(flask.render_template(
            'trace.html',
            places=places,
            journals=journals,
            option="mytrace"))
   return resp

@app.route('/placemap', methods=["GET"])
def get_my_place_map():
   uid = request.args.get('uid', "1")
   app.logger.debug("Accessing placemap.html %s", uid)
   
   places = getMyPlaces(uid)

   resp = flask.make_response(flask.render_template(
            'map.html',
            places=places,
            option="mytrace"))
   return resp

@app.route('/exploremap', methods=["GET"])
def get_explored_place_map():
   uid = request.args.get('uid', "1")
   app.logger.debug("Accessing placemap.html %s", uid)
   geo_info = {}
   geo_info['lat'] = request.args.get('lat', "")
   geo_info['long'] = request.args.get('long', "")
   
   places = getExploredPlaces(uid, geo_info)

   resp = flask.make_response(flask.render_template(
            'map.html',
            places=places,
            option="explore"))
   return resp

@app.route('/placedetail', methods=["GET"])
def get_place_detal():
   cid = request.args.get('cid', "1")
   app.logger.debug("Accessing placedetail.html %s", cid)
   
   place_info = getPlaceDetail(cid)

   resp = flask.make_response(flask.render_template(
            'placedetail.html',
            place_info=place_info,
            option="mytrace"))
   return resp

@app.route('/exploredplacedetail', methods=["GET"])
def get_explored_place_detal():
   cid = request.args.get('cid', "1")
   app.logger.debug("Accessing exploredplacedetail.html %s", cid)
   
   place_info = getPlaceDetail(cid)

   resp = flask.make_response(flask.render_template(
            'placedetail.html',
            place_info=place_info,
            option="explore"))
   return resp

@app.route('/journaldetail', methods=["GET"])
def get_journal_detal():
   jid = request.args.get('jid', "1")
   app.logger.debug("Accessing journaldetail.html %s", jid)
   
   journal_info = getJournalDetail(jid)

   resp = flask.make_response(flask.render_template(
            'journaldetail.html',
            journal_info=journal_info))
   return resp

@app.route('/capture')
def capture():
   uid = request.args.get('uid', "1")
   app.logger.debug("Accessing capture.html %s", uid)
   user = getUser(uid)
   now_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   friends = getFriends(uid)
   places = getPlaces()
   resp = flask.make_response(flask.render_template(
            'capture.html',
            user=user,
            now_datetime=now_datetime,
            places=places,
            friends=friends))
   return resp

@app.route('/saveplace', methods=["POST"])
def save_my_place():
   # get args
   uid = request.args.get('uid', "1")
   now_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   date_time = request.form.get('dateTime', now_datetime)
   pic_url = request.form.get('picUrl', "")
   comment = request.form.get('selfComment', "")
   travel_party = request.form.get('travelParty', "")
   perm = request.form.get('shareOption', "public")
   place_id = request.form.get('placeId', "1")
   flag = request.form.get('flag', "")
   app.logger.debug("Accessing saveplace.html, datetime: %s", date_time)
   app.logger.debug("Accessing saveplace.html, pic_url: %s", pic_url)
   app.logger.debug("Accessing saveplace.html, comment: %s", comment)
   app.logger.debug("Accessing saveplace.html, travel_party: %s", travel_party)
   app.logger.debug("Accessing saveplace.html, perm: %s", perm)
   app.logger.debug("Accessing saveplace.html, place_id: %s", place_id)

   # save place
   cid = saveMyPlace(uid, date_time, pic_url, comment, travel_party, perm, place_id)
   
   app.logger.debug("Accessing saveplace.html, checkin! cid: %s", cid)
   if flag == "create_journal":
       app.logger.debug("Accessing saveplace.html, call from createjournal, cid: %s", cid)
       checkin_info = {}
       checkin_info['cid'] = cid
       resp = flask.json.dumps(checkin_info)
       return resp
   else:
       return flask.redirect(flask.url_for('capture'))

'''
@app.route('/previewjournaldetail', methods=["POST"])
def preview_journal_detail():
    return
'''

@app.route('/previewjournal', methods=["POST"])
def preview_journal():
   # get args
   uid = request.args.get('uid', "1")
   now_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   date_time = request.form.get('dateTime', now_datetime)
   title = request.form.get('title', "")
   desp = request.form.get('desp', "")
   cids = request.form.get('cids', "")
   tmp_cids = request.form.get('tmp_cids', "")
   perm = request.form.get('shareOption', "public")
   app.logger.debug("Accessing previewjournal.html, datetime: %s", date_time)
   app.logger.debug("Accessing previewjournal.html, title: %s", title)
   app.logger.debug("Accessing previewjournal.html, desp: %s", desp)
   app.logger.debug("Accessing previewjournal.html, cids: %s", cids)
   app.logger.debug("Accessing previewjournal.html, tmp_cids: %s", tmp_cids)
   app.logger.debug("Accessing previewjournal.html, perm: %s", perm)

   # save journal
   jid = saveMyJournal(uid, date_time, title, desp, perm, cids, tmp_cids)

   # show journal
   journal_info = getJournalDetail(jid)
   resp = flask.make_response(flask.render_template(
            'journaldetail.html',
            journal_info=journal_info,
            tmp_cids=tmp_cids,
            option="previewjournal"))
   return resp

@app.route('/deljournal', methods=["POST"])
def del_my_journal():
   uid = request.form.get('uid', 1)
   jid = request.form.get('jid', "")
   tmp_cids = request.form.get('tmp_cids', "")
   app.logger.debug("Accessing deljournal.html %s %s %s", uid, jid, tmp_cids)

   delMyJournal(uid, jid, tmp_cids)

   return ""

@app.route('/editplace', methods=["GET"])
def edit_my_place():
   uid = request.args.get('uid', "1")
   cid = request.args.get('cid', "1")
   app.logger.debug("Accessing editplace.html %s", cid)

   place_info = getPlaceDetail(cid)
   friends = getFriends(uid)
   places = getPlaces()

   resp = flask.make_response(flask.render_template(
            'editplace.html',
            place_info=place_info,
            places=places,
            friends=friends))
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

@app.route('/createjournal')
def create_journal():
   uid = request.args.get('uid', "1")
   app.logger.debug("Accessing createjournal.html %s", uid)
   places = getMyPlaces(uid)
   resp = flask.make_response(flask.render_template(
            'createjournal.html',
            places=places))
   return resp

@app.route('/uploadphoto', methods=["POST"])
def upload_photo():
   app.logger.debug("Accessing uploadphoto")
   photo_info = {}
   photo_data = request.form.get('data', "")
   if photo_data != "":
      photo_info = FlickrUpload(photo_data)
   resp = flask.json.dumps(photo_info)
   return resp

@app.route('/getplacename', methods=["GET"])
def get_place_name():
   lat = request.args.get('lat', "")
   lng = request.args.get('lng', "")
   app.logger.debug("Accessing getplacename %s, %s" % (lat, lng))
   # first check local DB
   place_info = getPlaceByGeo(lat, lng)
   if place_info == {}:
       # else check Flickr
       place_info = FlickrGetPlaceName(lat, lng)

   resp = flask.json.dumps(place_info)
   return resp


if __name__ == "__main__":
   app.run()
