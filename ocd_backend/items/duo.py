from pprint import pprint
from copy import deepcopy
import urlparse
import json

import redis

from ocd_backend import settings
from ocd_backend.items import BaseItem
from ocd_backend.utils.misc import slugify, make_hash, get_file_encoding
from ocd_backend.utils.duo_csv import UnicodeReaderAsSlugs

class DuoBaseItem(BaseItem):
    #: Allowed key-value pairs for the document inserted in the 'combined index'
    combined_index_fields = {
        'hidden': bool,
        'id': unicode,
        'name': unicode,
        'fields': list,
        'data': list,
        'media_urls': list,
        'all_text': unicode
    }


class DuoItem(DuoBaseItem):
    def get_original_object_id(self):
        return unicode(make_hash(self.original_item['id']))

    def get_object_id(self):
        return unicode(make_hash(self.original_item['id']))

    def get_original_object_urls(self):
        return {
            "html": unicode(self.original_item['page']),
            "csv": unicode(self.original_item['file'])
        }

    def get_rights(self):
        return u'undefined'

    def get_collection(self):
        return u'DUO'  # not used

    def get_combined_index_data(self):
        # moved to the loader due to big (nested) files
        fields = []
        data = []

        combined_index_data = {
            'id': self.original_item['id'],
            'name': self.original_item['id'],
            'hidden': self.source_definition['hidden'],
            'fields': fields,
            'data': data,
            'media_urls': [],
            'all_text': self.get_all_text()
        }

        return combined_index_data

    def get_index_data(self):
        return {}

    def get_all_text(self):
        text_items = []

        return u' '.join(text_items)
