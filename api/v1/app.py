#!/usr/bin/python3
"""
    App module
"""
from api import storage
from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv
from api.v1.views import app_views

app = Flask(__name__)
host = getenv('HBNB_API_HOST') if (getenv('HBNB_API_HOST')) else '0.0.0.0'
port = getenv('HBNB_API_PORT') if (getenv('HBNB_API_PORT')) else 5000
app.register_blueprint(app_views)
CORS(app, resources={r'/*': {"origins": host}})


@app.teardown_appcontext
def teardown_app(exception):
    """
        closes the storage
    """
    storage.close()


@app.errorhandler(404)
@app.route('/nop', strict_slashes=False)
def handleErr(e):
    """ returns a JSON-formatted 404 status code response."""
    msg = {'error': 'Not found'}
    return (jsonify(msg), 404)


if __name__ == '__main__':
    app.run(host, port, threaded=True)
