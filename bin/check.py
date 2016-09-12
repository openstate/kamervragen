#!/usr/bin/env python

import os
import sys
import re
from pprint import pprint
import json
import requests

sys.path.insert(0, './')

from ocd_backend.utils.misc import slugify, make_hash_filename

API_URL = 'http://localhost:5000/v0'
ES_URL = 'http://localhost:9200/'

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def get_all_datasets():
    return requests.get(
        '%s/search' % (API_URL)
    ).json()

def get_dataset_num_rows(dataset_name):
    payload = {
        "query": {
            "constant_score" : {
                "filter" : {
                    "term" : { "_type" : slugify(dataset_name)}
                },
                "boost" : 1.0
            }
        },
        "size": 0
    }

    res = requests.post(
        '%s/duo_data_items/_search' % (ES_URL,), data=json.dumps(payload)
    ).json()
    return res['hits']['total']

def get_csv_num_rows(dataset_url):
    hashed_file_path = make_hash_filename(dataset_url.strip())
    hashed_full_path = os.path.join('/opt/duo/downloads', hashed_file_path)
    return file_len(hashed_full_path)
    #return requests.get(dataset_url).content.count('\n') + 1

def main():
    datasets = get_all_datasets()
    for dataset in datasets['hits']['hits']:
        num_es = get_dataset_num_rows(dataset['id'])
        num_csv = get_csv_num_rows(dataset['meta']['original_object_urls']['csv'])
        hashed_file_path = make_hash_filename(dataset['meta']['original_object_urls']['csv'].strip())
        print "%s\t%s\t%s\t%s\t\t%s (%s)" % (
            hashed_file_path, num_es, num_csv,num_csv-num_es, dataset['id'], slugify(dataset['id']))

if __name__ == '__main__':
    main()
