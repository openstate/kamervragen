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

    def search_questions(self, query=None):
        es_query = {
            "sort": "date",
            "order": "desc"
        }

        if query is not None:
            es_query['query'] = query

        return requests.post(
            '%s/tk_questions/search' % (self.URL,),
            data=json.dumps(es_query)).json()

api = BackendAPI()


@app.route("/")
def main():
    results = api.search_questions()
    return render_template('index.html', results=results)


@app.route("/zoeken")
def search():
    results = api.search_questions(request.args.get('query', None))
    return render_template('search_results.html', results=results)


def create_app():
    return app
