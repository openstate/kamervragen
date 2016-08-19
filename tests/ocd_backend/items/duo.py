import json
import os

from ocd_backend.items.duo import DuoItem

from . import ItemTestCase

class DuoItemTestCase(ItemTestCase):
    def setUp(self):
        super(DuoItemTestCase, self).setUp()
        self.PWD = os.path.dirname(__file__)
        dump_path = os.path.abspath(os.path.join(self.PWD, '../test_dumps/ocd_openbeelden_test.gz'))
        self.source_definition = {
            "id": "update",
            "extractor": "ocd_backend.extractors.duo.DUOCSVListExtractor",
            "transformer": "ocd_backend.transformers.BaseTransformer",
            "item": "ocd_backend.items.duo.DuoItem",
            "enrichers": [],
            "loader": "ocd_backend.loaders.DummyLoader",
            "cleanup": "ocd_backend.tasks.CleanupElasticsearch",
            "hidden": True,
            "index_name": "data",
            "doc_type": "files",
            "keep_index_on_update": True,
            "csv_file": "/opt/duo/files.csv",
            "csv_url_field": "bestand",
            "csv_page_field": "pagina",
            "csv_download_path": "/opt/duo/downloads"
        }


        with open(os.path.abspath(os.path.join(self.PWD, '../test_dumps/duo.json')), 'r') as f:
            self.raw_item = f.read()
        with open(os.path.abspath(os.path.join(self.PWD, '../test_dumps/duo.json')), 'r') as f:
            self.item = json.load(f)

        self.collection = u'DUO'
        self.rights = u'undefined'
        self.original_object_id = u'378ec38535e21cd942bca13422637e6c'
        self.original_object_urls = {
            u'html': u'https://www.duo.nl/open_onderwijsdata/databestanden/vo/adressen/adressen_vo_1.jsp',
            u'csv': u'https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv'
        }

    def _instantiate_item(self):
        return DuoItem(self.source_definition, 'application/json',
                             self.raw_item, self.item)

    def test_item_collection(self):
        item = self._instantiate_item()
        self.assertEqual(item.get_collection(), self.collection)

    def test_get_rights(self):
        item = self._instantiate_item()
        self.assertEqual(item.get_rights(), self.rights)

    def test_get_original_object_id(self):
        item = self._instantiate_item()
        self.assertEqual(item.get_original_object_id(), self.original_object_id)


    def test_get_original_object_urls(self):
        item = self._instantiate_item()
        self.assertDictEqual(item.get_original_object_urls(),
                             self.original_object_urls)


    def test_get_combined_index_data(self):
        item = self._instantiate_item()
        self.assertIsInstance(item.get_combined_index_data(), dict)

    def test_get_index_data(self):
        item = self._instantiate_item()
        self.assertIsInstance(item.get_index_data(), dict)

    def test_get_all_text(self):
        item = self._instantiate_item()
        self.assertEqual(type(item.get_all_text()), unicode)
        #self.assertTrue(len(item.get_all_text()) > 0)

    def test_combined_index_data_types(self):
        item = self._instantiate_item()
        data = item.get_combined_index_data()
        for field, field_type in item.combined_index_fields.iteritems():
            self.assertIn(field, data)
            self.assertIsInstance(data[field], field_type)
