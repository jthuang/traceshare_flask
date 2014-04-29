import flask
from os import environ

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

@app.route('/myplace', methods=["GET"])
def get_my_place():
    app.logger.debug("Accessing myPlace.html")
    resp = flask.make_response(flask.render_template('myPlaces.html'))
    return resp

@app.route('/placeEdit', methods=["GET"])
def get_my_place():
    app.logger.debug("Accessing placeEdit.html")
    resp = flask.make_response(flask.render_template('placeEdit.html'))
    return resp


