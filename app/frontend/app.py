import simplejson as json

from flask import (
    Flask, abort, jsonify, request, redirect, render_template,
    stream_with_context, Response)
import requests


app = Flask(__name__)


class BackendAPI(object):
    URL = 'http://c-tkv-nginx/v0'

    def sources(self):
        return requests.get('%s/sources' % (self.URL,)).json()

api = BackendAPI()


@app.route("/")
def main():
    return render_template('index.html', sources=None)


@app.route("/zoeken")
def search():
    sources = api.sources()
    return render_template('index.html', sources=sources)


def create_app():
    return app
