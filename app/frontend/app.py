import simplejson as json

from flask import (
    Flask, abort, jsonify, request, redirect, stream_with_context, Response)

app = Flask(__name__)
app.config['SERVER_NAME'] = 'api.duo.nl'

@app.route("/")
def main():
    return "Hello World!"

def create_app():
    return app
