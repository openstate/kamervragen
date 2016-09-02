import datetime
import os
from unittest import TestCase

from ocd_backend import settings
from ocd_backend.es import elasticsearch as es
from ocd_backend.pipeline import (
    get_alias_for_source, get_timed_index_name_for_alias, get_current_index,
    initialize_index, get_new_index)
from ocd_backend.exceptions import ConfigurationError

class PipelineMiscTestCase(TestCase):
    def setUp(self):
        super(PipelineMiscTestCase, self).setUp()
        self.source_definition = {
            'id': 'test_source',
            'index_name': 'test_data',
            'keep_index_on_update': False
        }
        self.index_alias = 'duo_test_data'
        self.index_no_index_name = 'duo_test_source'
        self.dated = datetime.datetime(2016, 12, 31, 1, 2, 3)
        self.dated_index_name = 'duo_test_data_20161231010203'
        self.dated_combined_index_name = 'duo_combined_index_20161231010203'

        self.combined_source_definition = {
            'id': 'test_source',
            'index_name': 'combined_index',
            'keep_index_on_update': False
        }

    def test_get_alias_for_source(self):
        result = get_alias_for_source(self.source_definition)
        self.assertEqual(result, self.index_alias)

    def test_get_alias_for_combined(self):
        result = get_alias_for_source(self.combined_source_definition)
        self.assertEqual(result, settings.COMBINED_INDEX)

    def test_get_alias_for_source_no_index_name(self):
        del self.source_definition['index_name']
        result = get_alias_for_source(self.source_definition)
        self.assertEqual(result, self.index_no_index_name)

    def test_get_timed_index_name_for_alias(self):
        result = get_timed_index_name_for_alias(self.index_alias, self.dated)
        self.assertEqual(result, self.dated_index_name)

    def test_get_timed_index_name_for_alias_combined(self):
        result = get_timed_index_name_for_alias(settings.COMBINED_INDEX, self.dated)
        self.assertEqual(result, self.dated_combined_index_name)

    def test_get_current_index(self):
        es.indices.create(self.dated_index_name)
        es.indices.put_alias(
            name=self.index_alias, index=self.dated_index_name)
        result = get_current_index(self.index_alias)
        self.assertTrue(result, self.dated_index_name)
        # cleanup
        es.indices.delete_alias(name=self.index_alias, index=self.dated_index_name)
        es.indices.delete(self.dated_index_name)

    def test_get_current_index_no_alias(self):
        with self.assertRaises(ConfigurationError):
            result = get_current_index(self.index_alias)

    def test_initialize_index(self):
        result = initialize_index(self.source_definition, self.dated)
        self.assertEqual(result, self.index_alias)
        current_index = get_current_index(self.index_alias)
        self.assertEqual(current_index, self.dated_index_name)
        # cleanup
        es.indices.delete_alias(name=self.index_alias, index=current_index)
        es.indices.delete(current_index)

    def test_initialize_index_combined(self):
        result = initialize_index(self.combined_source_definition, self.dated)
        self.assertEqual(result, settings.COMBINED_INDEX)
        current_index = get_current_index(settings.COMBINED_INDEX)
        self.assertEqual(current_index, self.dated_combined_index_name)
        # cleanup
        es.indices.delete_alias(name=settings.COMBINED_INDEX, index=current_index)
        es.indices.delete(current_index)

    def test_get_new_index(self):
        result = get_new_index(
            self.source_definition, self.index_alias, self.index_alias,
            self.dated)
        self.assertEqual(result, self.dated_index_name)

    def test_get_new_index_keep(self):
        self.source_definition['keep_index_on_update'] = True
        result = get_new_index(
            self.source_definition, self.index_alias, self.index_alias,
            self.dated)
        self.assertEqual(result, self.index_alias)
