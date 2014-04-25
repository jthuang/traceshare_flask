import flask
from os import environ

app = flask.Flask(__name__)
app.debug = True

@app.route('/')
def hello():
    return 'Hello World! TraceShare!'

@app.route('/myplace', methods=["GET"])
def get_my_place:
    app.logger.debug("Redirecting to " + destination)
    resp = flask.make_response(flask.render_template('myPlaces.html')

    return resp


if __name__ == "__main__":
    app.run(port=int(environ['FLASK_PORT']))
