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

    def stats_questions(self):
        es_query = {
            "size": 0,
            "facets": {
                "dates": {
                    "interval": "year"
                }
            }
        }

        try:
            result = requests.post(
                '%s/tk_questions/search' % (self.URL,),
                data=json.dumps(es_query)).json()
        except Exception:
            result = {
                'facets': {
                    'dates': {
                        'entries': []
                    }
                },
                'hits': {
                    'hits': [],
                    'total': 0
                }
            }
        return result

    def search_questions(self, query=None):
        es_query = {
            "sort": "date",
            "order": "desc"
        }

        if query is not None:
            es_query['query'] = query

        try:
            result = requests.post(
                '%s/tk_questions/search' % (self.URL,),
                data=json.dumps(es_query)).json()
        except Exception:
            result = {
                'hits': {
                    'hits': [],
                    'total': 0
                }
            }
        return result

    def find_by_id(self, id):
        es_query = {
            "filters": {
                "id": {"terms": [id]}
            },
            "size": 1
        }

        return requests.post(
            '%s/tk_questions/search' % (self.URL,),
            data=json.dumps(es_query)).json()

api = BackendAPI()


@app.route("/")
def main():
    results = api.search_questions()
    return render_template('index.html', results=results)


@app.route("/stats")
def stats():
    results = api.stats_questions()
    return render_template('stats.html', results=results)


@app.route("/zoeken")
def search():
    results = api.search_questions(request.args.get('query', None))
    return render_template('search_results.html', results=results)


@app.route("/<period>/<id>")
def display(period, id):
    result = api.find_by_id(id)

    if result['meta']['total'] <= 0:
        abort(404)

    return render_template(
        'display_result.html', result=result['hits']['hits'][0])


def create_app():
    return app
