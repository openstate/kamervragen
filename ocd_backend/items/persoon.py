from datetime import datetime

from ocd_backend.items.popolo import PersonItem


class PersoonItem(PersonItem):
    namespaces = {
        'atom': 'http://www.w3.org/2005/Atom',
        'd': "http://schemas.microsoft.com/ado/2007/08/dataservices",
        'm': "http://schemas.microsoft.com/ado/2007/08/dataservices/metadata"
    }

    def _get_text_or_none(self, xpath_expression):
        node = self.original_item.find(
            xpath_expression, namespaces=self.namespaces)
        if node is not None and node.text is not None:
            return unicode(node.text)

        return None

    def get_original_object_id(self):
        return unicode(self._get_text_or_none('.//d:Id'))

    def get_object_id(self):
        return unicode(self._get_text_or_none('.//d:Id'))

    def get_original_object_urls(self):
        return {
            'xml': self._get_text_or_none('.//atom:id')
        }

    def get_collection(self):
        return u'Personen'

    def get_rights(self):
        return u'Unknown'

    def get_combined_index_data(self):
        combined_index_data = {}
        combined_index_data['id'] = self._get_text_or_none('.//d:Id')
        combined_index_data['hidden'] = self.source_definition['hidden']
        combined_index_data['identifiers'] = [
            {
                'scheme': 'Tweede Kamer',
                'identifier': self._get_text_or_none('.//d:Id')
            }
        ]
        name_parts = [
            self._get_text_or_none('.//d:Roepnaam') or self._get_text_or_none('.//d:Voornamen'),
            self._get_text_or_none('.//d:Tussenvoegsel'),
            self._get_text_or_none('.//d:Achternaam'),
        ]
        print name_parts
        combined_index_data['name'] = u' '.join(
            [n for n in name_parts if n is not None])
        combined_index_data['given_name'] = name_parts[0]
        combined_index_data['family_name'] = u' '.join(
            [n for n in name_parts[1:] if n is not None])
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
