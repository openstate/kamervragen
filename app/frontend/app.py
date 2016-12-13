import simplejson as json

from flask import (
    Flask, abort, jsonify, request, redirect, render_template,
    stream_with_context, Response)

app = Flask(__name__)


@app.route("/")
def main():
    return render_template('index.html')


def create_app():
    return app
