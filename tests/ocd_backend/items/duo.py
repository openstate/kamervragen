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
        # self.rights = u'Creative Commons Attribution-ShareAlike'
        # self.original_object_id = u'oai:openimages.eu:749181'
        # self.original_object_urls = {
        #     u'xml': u'http://openbeelden.nl/feeds/oai/?verb=GetRecord&identifie'
        #             u'r=oai:openimages.eu:749181&metadataPrefix=oai_oi',
        #     u'html': u'http://openbeelden.nl/media/749181/'
        # }

    def _instantiate_item(self):
        return DuoItem(self.source_definition, 'application/json',
                             self.raw_item, self.item)

    def test_item_collection(self):
        item = self._instantiate_item()
        self.assertEqual(item.get_collection(), self.collection)
