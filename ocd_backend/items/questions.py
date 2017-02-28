from datetime import datetime
from lxml import etree
from pprint import pprint

import iso8601

from ocd_backend.items import BaseItem
from ocd_backend.extractors import HttpRequestMixin
from ocd_backend.utils.api import FrontendAPIMixin
from ocd_backend.utils.to_text import FileToTextMixin

class OBWrittenQuestionItem(BaseItem, HttpRequestMixin):
    combined_index_fields = {
        'id': unicode,
        'hidden': bool,
        'identifiers': list,
        'classification': unicode,
        'name': unicode,
        'asked': datetime,
        'answered': datetime,
        'questions': list,
        'answers': list,
        'description': unicode,
    }

    def get_original_object_id(self):
        return unicode(self.original_item[u'link'])

    def get_original_object_urls(self):
        if self.original_item[u'link'].endswith('.html'):
            xml_link = self.original_item[u'link'].replace('.html', '.xml')
        else:
            xml_link = "%s.xml" % (self.original_item[u'link'],)
        return {
            'html': self.original_item[u'link'],
            'xml': xml_link
        }

    def get_collection(self):
        return self.original_item[u'category']

    def get_rights(self):
        return u'Unknown'

    def _get_xml(self):
        resp = self.http_session.get(
            self.get_original_object_urls()['xml'], verify=False)
        if resp.status_code >= 200 and resp.status_code < 300:
            return etree.fromstring(resp.content)
        return None

    def get_combined_index_data(self):
        # xml = self._get_xml()
        combined_index_data = {}
        combined_index_data['id'] = self.get_original_object_id()
        combined_index_data['hidden'] = self.source_definition['hidden']
        combined_index_data['name'] = self.original_item[u'description']
        try:
            xml = self._get_xml()
        except Exception as e:
            print str(e)
        combined_index_data['questions'] = []
        combined_index_data['answers'] = []

        if xml is None:
            return combined_index_data

        try:
            combined_index_data['asked'] = iso8601.parse_date(
                u''.join(xml.xpath(
                    '//kamervraagomschrijving[@type="vraag"]/datum/@isodatum')
                    ))
        except Exception:
            pass
        try:
            combined_index_data['answered'] = iso8601.parse_date(
                u''.join(xml.xpath(
                    '//kamervraagomschrijving[@type="antwoord"]/datum/@isodatum')
                    ))
        except Exception:
            pass

        try:
            for question in xml.xpath('//vraag'):
                combined_index_data['questions'].append({
                    u'number': u''.join(question.xpath('.//nr//text()')),
                    u'question': u''.join(question.xpath('.//al//text()'))
                })
        except Exception as e:
            print str(e)

        try:
            for question in xml.xpath('//antwoord'):
                combined_index_data['answers'].append({
                    u'number': u''.join(question.xpath('.//nr//text()')),
                    u'answer': u''.join(question.xpath('.//al//text()'))
                })
        except Exception as e:
            print str(e)

        combined_index_data['identifiers'] = [
            {
                'scheme': 'Tweede Kamer',
                'identifier': u''.join(xml.xpath('//kamervraagnummer//text()'))
            }
        ]

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


class TKWrittenQuestionItem(
    BaseItem, HttpRequestMixin, FrontendAPIMixin, FileToTextMixin
):
    combined_index_fields = {
        'id': unicode,
        'hidden': bool,
        'identifiers': list,
        'classification': unicode,
        'name': unicode,
        'date': datetime,
        'period': unicode,
        'appendix': unicode,
        'description': unicode,
        'person_id': unicode,
        'person': dict,
        'organization_id': unicode,
        'organization': dict
    }

    def get_property(
            self, props, prop_name, property_field='value', default=None
    ):
        matched_props = [p for p in props if p['name'] == prop_name]
        try:
            return matched_props[0][property_field]
        except LookupError:
            return default

    def get_document_url(self, ref):
        return (
            u'https://gegevensmagazijn.tweedekamer.nl/OData/v1/Bestand'
            u'(guid\'%s\')/$value') % (ref,)

    def get_original_object_id(self):
        return unicode(self.get_property(
            self.original_item['content']['internal']['properties'],
            'id'))

    def get_object_id(self):
        return unicode(self.get_property(
            self.original_item['content']['internal']['properties'],
            'id'))

    def get_original_object_urls(self):
        return {
        }

    def get_collection(self):
        return u'Schriftelijke Vragen'

    def get_rights(self):
        return u'Unknown'

    def get_combined_index_data(self):
        combined_index_data = {}
        combined_index_data['id'] = self.get_property(
            self.original_item['content']['internal']['content'],
            'nummer', 'content')
        combined_index_data['hidden'] = self.source_definition['hidden']
        combined_index_data['identifiers'] = [
            {
                'scheme': 'Tweede Kamer',
                'identifier': self.get_original_object_id()
            }
        ]
        combined_index_data['classification'] = self.get_property(
            self.original_item['content']['internal']['content'],
            'soort', 'content')
        combined_index_data['name'] = self.get_property(
            self.original_item['content']['internal']['content'],
            'onderwerp', 'content')
        combined_index_data['date'] = datetime.strptime(self.get_property(
            self.original_item['content']['internal']['content'],
            'datum', 'content'), '%Y-%m-%d')
        combined_index_data['period'] = self.get_property(
            self.original_item['content']['internal']['content'],
            'vergaderjaar', 'content')
        combined_index_data['appendix'] = self.get_property(
            self.original_item['content']['internal']['content'],
            'aanhangselnummer', 'content')

        # get associated file with contents
        try:
            ref = [p for p in self.get_property(
                self.original_item['content']['internal']['content'],
                'bestand', 'properties') if p['name'] == 'ref'][0]['value']
        except LookupError:
            ref = None

        if ref is not None:
            combined_index_data['description'] = self.text_get_contents(
                self.get_document_url(ref),
                self.source_definition.get('pdf_max_pages', 20))

        print "All done for this item!"
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


class TKWrittenAnswerItem(TKWrittenQuestionItem):
    def get_collection(self):
        return u'Antwoorden'
