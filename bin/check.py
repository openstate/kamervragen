#!/usr/bin/env python

import os
import sys
import re
from pprint import pprint
import json
import requests

API_URL = 'http://localhost:5000/v0'

def get_all_datasets():
    return requests.get(
        '%s/search' % (API_URL)
    ).json()

def get_dataset_num_rows(dataset_name):
    payload = {
        'include_fields': ['data', 'fields'],
        'filters': {
            'id': {
                'terms': [dataset_name]
            }
        }
    }

    res = requests.post(
        '%s/search' % (API_URL,), data=json.dumps(payload)
    ).json()
    return len(res['hits']['hits'][0]['data'])

def get_csv_num_rows(dataset_url):
    return requests.get(dataset_url).content.count('\n') + 1

def main():
    datasets = get_all_datasets()
    for dataset in datasets['hits']['hits']:
        num_es = get_dataset_num_rows(dataset['id'])
        num_csv = get_csv_num_rows(dataset['meta']['original_object_urls']['csv'])
        print "%-40s\t%s\t%s\t%s" % (
            dataset['id'], num_es, num_csv,num_csv-num_es)

if __name__ == '__main__':
    main()
