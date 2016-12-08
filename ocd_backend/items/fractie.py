# from datetime import datetime
from pprint import pprint

from ocd_backend.items.popolo import OrganisationItem


class FractieItem(OrganisationItem):
    def get_property(
            self, props, prop_name, property_field='value', default=None
    ):
        matched_props = [p for p in props if p['name'] == prop_name]
        try:
            return matched_props[0][property_field]
        except LookupError:
            return default

    def get_original_object_id(self):
        return unicode(self.get_property(
            self.original_item['content']['internal']['properties'],
            'id'))

    def get_original_object_urls(self):
        return {
        }

    def get_collection(self):
        return u'Personen'

    def get_rights(self):
        return u'Unknown'

    def get_combined_index_data(self):
        combined_index_data = {}
        combined_index_data['id'] = self.get_original_object_id()
        combined_index_data['hidden'] = self.source_definition['hidden']
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
