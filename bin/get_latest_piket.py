#!/usr/bin/env python

import os
import sys
import re

import requests
from redis import StrictRedis


def _get_feed_url(url):
    return requests.get(
        url.replace(u'/REST/Feed?', u'/REST/Feed.json?'), headers={
            'Authorization': (
                'Basic dG9ta3VuemxlcjpEUk4kTyRrelF4NUVaaCVsem03YQ==')
        }, verify=False)


def main():
    client = StrictRedis()
    latest_piket_url = client.get('tk_piketpaaltje_url_tk_questions')
    print _get_feed_url(latest_piket_url).content
    return 0

if __name__ == '__main__':
    sys.exit(main())
