from pprint import pprint
from copy import deepcopy

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
    def _process_row(self, row):
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
        return deepcopy(row)

    def _get_data(self):
        """
        Loads the data from the CSV file (on disk) and returns the data
        structure for the data itself and the field definitions.
        """
        fields = []
        data = []
        # FIXME: this way of getting the encoding is way to slow
        # encoding = get_file_encoding(self.original_item['local_filename'])['encoding']
        encoding= 'iso-8859-1'
        with open(self.original_item['local_filename']) as csvfile:
            reader = UnicodeReaderAsSlugs(csvfile, delimiter=';', encoding=encoding)
            fields = [{'key': k, 'name': k, 'label': l} for k,l in reader.header_map.iteritems()]
            fields += [{'key': unicode(k), 'name': unicode(k), 'label': unicode(k)} for k in self.source_definition['fields_mapping']]
            data = [self._process_row(r) for r in reader]
        data = []
        return fields, data

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
        try:
            fields, data = self._get_data()
        except (ValueError, LookupError) as e:  # TODO: what kind of errors could there be?
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
