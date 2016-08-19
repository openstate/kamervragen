from ocd_backend.items import BaseItem
from ocd_backend.utils.misc import slugify, make_hash

class DuoBaseItem(BaseItem):
    #: Allowed key-value pairs for the document inserted in the 'combined index'
    combined_index_fields = {
        'hidden': bool,
        'id': unicode,
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
        combined_index_data = {
            'id': self.original_item['id'],
            'hidden': self.source_definition['hidden'],
            'fields': [],
            'data': [],
            'media_urls': []
        }

        return combined_index_data

    def get_index_data(self):
        return {}

    def get_all_text(self):
        text_items = []

        return u' '.join(text_items)
