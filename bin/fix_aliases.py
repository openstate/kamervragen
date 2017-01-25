#!/usr/bin/env python
import os
import sys
import re
from pprint import pprint
import json
from time import sleep

from redis import StrictRedis

sys.path.insert(0, './')

from ocd_backend.es import elasticsearch
from ocd_backend import settings

def fix_aliases():
    sleep(5)
    indices = [x for x in re.split(r'\s+', elasticsearch.cat.indices()) if x.startswith('%s_' % (settings.DEFAULT_INDEX_PREFIX,))]
    print "Found indices:"
    print indices
    for idx in ['combined_index', 'tk_questions']:
        idx_indices = sorted([x for x in indices if x.startswith('%s_%s_' % (settings.DEFAULT_INDEX_PREFIX, idx,))])
        newest_index = idx_indices[-1]
        alias = '%s_%s' % (settings.DEFAULT_INDEX_PREFIX, idx,)
        previous_index = elasticsearch.indices.get_alias(alias).keys()[0]

        if newest_index == previous_index:
            continue

        print "%s -> %s" % (newest_index, previous_index,)

        actions = {'actions': []}
        actions['actions'] += [
            {
                'remove': {
                    'index': previous_index,
                    'alias': alias
                }
            },
            {
                'add': {
                    'index': newest_index,
                    'alias': alias
                }
            }
        ]

        # Set alias to new index
        elasticsearch.indices.update_aliases(body=actions)

def main():
    redis = StrictRedis()
    pipelines = redis.keys('pipeline_*')
    all_done = True
    for pipeline in pipelines:
        # ignore chains
        if pipeline.endswith('_chains'):
            all_done = False
            continue
        pipeline_chains = '%s_chains' % (pipeline,)
        # but do check if there is an accompanying chain (still running)
        if pipeline_chains in pipelines:
            all_done = False
            continue
        pipeline_status = redis.get(pipeline)
        print "Pipeline %s is %s" % (pipeline, pipeline_status,) 
        all_done = all_done and (pipeline_status == 'done')

    if all_done:
        fix_aliases()


if __name__ == '__main__':
    main()
