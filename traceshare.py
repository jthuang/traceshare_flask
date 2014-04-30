import flask
from flask import request
from os import environ
from getMyPlaces import getMyPlaces

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
   app.logger.debug("Accessing mytrace.html")
   
   # TODO: get uid from GET argument
   uid = "1"
   places = getMyPlaces(uid)

   place_list = []
   for p in places:
      place_list.append((p['cid'], p['time'], p['place_id'], p['photo_url'], p['place_name']))

   resp = flask.make_response(flask.render_template(
            'mytrace.html',
            place_list=place_list))
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
