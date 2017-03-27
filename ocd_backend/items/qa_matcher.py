from datetime import datetime, timedelta
from pprint import pprint
from operator import itemgetter
import traceback

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
        'organization': dict,
        'questions_hash': unicode,
        'questions': unicode,
        'answer': dict
    }

    def __init__(self, source_definition, data_content_type, data, item,
                 processing_started=None):
        try:
            super(QaMatcherItem, self).__init__(
                source_definition, data_content_type, data, item,
                processing_started)
        except Exception as e:
            print e
            traceback.print_exc()
        sh = getInstance()
        name_shingles = sh.wshingling(self.original_item['name'])
        if 'questions' in self.original_item:
            question_shingles = sh.wshingling(self.original_item['questions'])
        else:
            question_shingles = None
        docs = self.get_candidate_documents()
        try:
            self.match = self.get_top_candidate(
                sh, name_shingles, question_shingles, docs)
        except Exception as e:
            print e
            traceback.print_exc()

        try:
            if getattr(self, 'match', None) is not None:
                print "ANTWOORD: %s - %s" % (
                    self.match['date'], self.match['name'],)

            # On init, all data should be available to construct self.meta
            # and self.combined_item
            self._construct_object_meta(processing_started)
            self._construct_combined_index_data()

            self.index_data = self.get_index_data()
        except Exception as e:
            print e
            traceback.print_exc()

    def jc_sim(self, shingles, doc_shingles):
        intersection = []
        union = []
        str_shingles = [u' '.join(x) for x in shingles]
        str_doc_shingles = [u' '.join(x) for x in doc_shingles]
        intersection = list(set(str_shingles) & set(str_doc_shingles))
        union = list(set(str_shingles) | set(str_doc_shingles))
        return float(len(intersection))/float(len(union))

    def get_top_candidate(self, sh, name_shingles, question_shingles, docs):
        scores = []
        for doc in docs:
            # if (
            #     ('questions' not in doc) or
            #     (doc['questions'].strip == u'')
            # ):
            #     doc_shingles = sh.wshingling(doc['name'])
            #     jc_sim = self.jc_sim(name_shingles, doc_shingles)
            # else:
            #     doc_shingles = sh.wshingling(doc['questions'])
            #     try:
            #         jc_sim = self.jc_sim(
            #             question_shingles, doc_shingles)
            #     except TypeError:
            #         jc_sim = 0.0
            doc_shingles = sh.wshingling(doc['name'])
            jc_sim = self.jc_sim(name_shingles, doc_shingles)
            if jc_sim > 0.0:
                scores.append((jc_sim, doc,))
        try:
            return max(scores, key=itemgetter(0))[1]
        except ValueError:
            return None

    def get_candidate_documents(self):
        print "VRAAG: %s - %s" % (
            self.original_item['date'], self.original_item['name'],)
        date = self.original_item['date']
        start_date = date + timedelta(days=90)
        candidates = []
        results_count = 1
        offset = 0
        page_size = 100
        api_args = {
            'date': {
                'from': date.isoformat(),
                'to': start_date.isoformat()
            },
            'from': offset,
            'size': page_size
        }
        args = (
            self.source_definition['match_index_name'],
            self.source_definition['match_doc_type'])
        while results_count > 0:
            results = self.api_request(*args, **api_args)
            candidates += results['hits']['hits']
            results_count = len(results['hits']['hits'])
            offset += results_count
            api_args['from'] = offset
        # for candidate in candidates:
        #     print "KANDIDAAT: %s - %s" % (candidate['date'], candidate['name'],)
        return candidates

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
        combined_index_data = self.original_item
        if 'meta' in combined_index_data:
            del combined_index_data['meta']
        if isinstance(combined_index_data['date'], basestring):
            combined_index_data['date'] = iso8601.parse_date(
                combined_index_data['date'])
        combined_index_data['hidden'] = self.source_definition['hidden']

        self_match = getattr(self, 'match', None)

        if self_match is not None:
            combined_index_data['answer'] = self_match

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
