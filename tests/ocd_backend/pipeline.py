import os
from unittest import TestCase
from pprint import pprint

from ocd_backend.pipeline import get_alias_for_source

class PipelineMiscTestCase(TestCase):
    def setUp(self):
        super(PipelineMiscTestCase, self).setUp()
        self.source_definition = {
            'id': 'test_source',
            'index_name': 'data'
        }
        self.index_alias = 'duo_data'
        self.index_no_index_name = 'duo_test_source'

    def test_get_alias_for_source(self):
        result = get_alias_for_source(self.source_definition)
        self.assertEqual(result, self.index_alias)

    def test_get_alias_for_source_no_index_name(self):
        del self.source_definition['index_name']
        result = get_alias_for_source(self.source_definition)
        self.assertEqual(result, self.index_no_index_name)
