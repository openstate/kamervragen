from pprint import pprint
from copy import deepcopy
import urlparse
import json
import os
import re

import redis
from elasticsearch.helpers import bulk

from ocd_backend import settings
from ocd_backend.es import elasticsearch
from ocd_backend.items import BaseItem
from ocd_backend.utils.misc import slugify, make_hash, get_file_encoding, make_hash_filename
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

    def _process_row(self, item_id, row, row_index, index_name):
        """
        Adds the uni fields from the row data that was given. The uni fields are
        defined in the source definition.
        """
        for uni_field in self.source_definition['fields_mapping']:
            for source_field in self.source_definition['fields_mapping'][uni_field]:
                try:
                    row[uni_field] = row[source_field]
                except LookupError as e:
                    pass
        row['hidden'] = self.source_definition['hidden']
        row['meta'] = {
            'row': row_index,
            'source_id': item_id
        }
        return [{
            '_id': u'%s-%s' % (slugify(item_id), row_index,),
            '_index': index_name,
            '_type': slugify(item_id),
            '_source': row
        }]

    def _get_field_definitions(self, header_map, fields_mapping):
        """
        Gets the field mapping for a dataset
        """
        fields = [{'key': k, 'name': k, 'label': l} for k,l in header_map.iteritems()]
        for k,v in fields_mapping.iteritems():
            fields += [{'key': unicode(k), 'name': unicode(k), 'label': unicode(k)} for f in v if f in header_map.values()]
        return fields

    def _get_data(self, csv_url, item_id):
        """
        Loads the data from the CSV file (on disk) and returns the data
        structure for the data itself and the field definitions.
        """
        fields = []
        data = []
        # FIXME: this way of getting the encoding is way to slow
        # encoding = get_file_encoding(self.original_item['local_filename'])['encoding']
        encoding= 'iso-8859-1'
        local_filename = os.path.join(
            self.source_definition['csv_download_path'],
            make_hash_filename(csv_url))
        # ugly hack to get the index we should write to

        indices = [x for x in self.source_definition['params']['new_index_names'] if x.startswith('duo_data_items')]
        data_items_index_name = indices[0]
        pprint(data_items_index_name)
        with open(local_filename) as csvfile:
            reader = UnicodeReaderAsSlugs(csvfile, delimiter=';', encoding=encoding)
            fields = self._get_field_definitions(reader.header_map, self.source_definition['fields_mapping'])
            row_count = 0
            for r in reader:
                data += self._process_row(
                    item_id, r, row_count, data_items_index_name)
                row_count += 1
        return fields, data

    def get_combined_index_data(self):
        try:
            fields, data = self._get_data(
                unicode(self.original_item['file']),
                unicode(self.original_item['id']))
        except (ValueError, LookupError) as e:  # TODO: what kind of errors could there be?
            fields = []
            data = []

        combined_index_data = {
            'id': self.original_item['id'],
            'name': self.original_item['id'],
            'hidden': self.source_definition['hidden'],
            'fields': fields,
            'data': [],
            'media_urls': [],
            'all_text': self.get_all_text()
        }

        bulk(elasticsearch, data, stats_only=True)

        return combined_index_data

    def get_index_data(self):
        return {}

    def get_all_text(self):
        text_items = []

        return u' '.join(text_items)
