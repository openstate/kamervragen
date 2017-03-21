import json
from pprint import pprint
import re

from ocd_backend.extractors import BaseExtractor, HttpRequestMixin
from ocd_backend.exceptions import ConfigurationError
from ocd_backend.utils.api import FrontendAPIMixin

from ocd_backend import settings


class FrontendAPIExtractor(BaseExtractor, HttpRequestMixin, FrontendAPIMixin):
    """
    Extracts items from the frontend API.
    """
    def run(self):
        index_name = (
            self.source_definition.get('frontend_index') or
            self.source_definition['index_name'])
        api_args = self.source_definition['frontend_args']
        api_results = 1
        api_page = 1
        # TODO: implement actual paging .... ;) (let's)
        while api_results > 0:
            print "Fetching page %s ..." % (api_page,)
            results = self.api_request(
                index_name,
                self.source_definition['frontend_type'],
                **api_args)   # 100 for now ...
            for result in results[u'hits'][u'hits']:
                print "%s - %s" % (result['name'], result['date'],)
                yield 'application/json', json.dumps(result)
            api_results = 0
