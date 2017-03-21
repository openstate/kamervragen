from datetime import datetime, timedelta
from pprint import pprint

from shingling import getInstance
import iso8601

from ocd_backend.items import BaseItem
from ocd_backend.extractors import HttpRequestMixin
from ocd_backend.utils.api import FrontendAPIMixin


class QaMatcherItem(
    BaseItem, HttpRequestMixin, FrontendAPIMixin
):
    combined_index_fields = {
        'id': unicode,
        'hidden': bool,
        'doc': dict,
    }

    def __init__(self, source_definition, data_content_type, data, item,
                 processing_started=None):
        super(QaMatcherItem, self).__init__(
            source_definition, data_content_type, data, item,
            processing_started)
        print "Init of QA matcher object ..."
        sh = getInstance()
        shingles = sh.wshingling(self.original_item['questions'])

    def get_original_object_id(self):
        return unicode(self.original_item['id'])

    def get_object_id(self):
        return unicode(self.original_item['id'])

    def get_original_object_urls(self):
        return {
        }

    def get_collection(self):
        return unicode(self.original_item.get(
            'collection', u'Schriftelijke Vragen'))

    def get_rights(self):
        return u'Unknown'

    def get_combined_index_data(self):
        combined_index_data = {
            'id': unicode(self.original_item['id']),
            'hidden': self.source_definition['hidden'],
            'doc': {}
        }
        return combined_index_data

    def get_index_data(self):
        return {}

    def get_all_text(self):
        text_items = []

        # # Title
        # text_items.append(self._get_text_or_none('.//dc:title'))
        #
        # # Creator
        # text_items.append(self._get_text_or_none('.//dc:creator'))
        #
        # # Subject
        # subjects = self.original_item.findall('.//dc:subject',
        #                                       namespaces=self.namespaces)
        # for subject in subjects:
        #     text_items.append(unicode(subject.text))
        return u' '.join([ti for ti in text_items if ti is not None])
