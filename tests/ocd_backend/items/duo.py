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
            "csv_download_path": "/opt/duo/downloads",
            "fields_mapping": {
                "uni_brin": ["brin_nummer", "brin_code"]
            }
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


        self.duo_id = u'01.-hoofdvestigingen-vo'
        self.duo_name = u'01.-hoofdvestigingen-vo'

        self.fields = [
            {'key': u"PROVINCIE", 'name': u"PROVINCIE", 'label': "provincie"},
            {'key': u"BEVOEGD GEZAG NUMMER", 'name': u"BEVOEGD GEZAG NUMMER", 'label': "bevoegd_gezag_nummer"},
            {'key': u"BRIN NUMMER", 'name': u"BRIN NUMMER", 'label': "brin_nummer"},
            {'key': u"INSTELLINGSNAAM", 'name': u"INSTELLINGSNAAM", 'label': "instellingsnaam"},
            {'key': u"STRAATNAAM", 'name': u"STRAATNAAM", 'label': "straatnaam"},
            {'key': u"HUISNUMMER-TOEVOEGING", 'name': u"HUISNUMMER-TOEVOEGING", 'label': "huisnummer_toevoeging"},
            {'key': u"POSTCODE", 'name': u"POSTCODE", 'label': "postcode"},
            {'key': u"PLAATSNAAM", 'name': u"PLAATSNAAM", 'label': "plaatsnaam"},
            {'key': u"GEMEENTENUMMER", 'name': u"GEMEENTENUMMER", 'label': "gemeentenummer"},
            {'key': u"GEMEENTENAAM", 'name': u"GEMEENTENAAM", 'label': "gemeentenaam"},
            {'key': u"DENOMINATIE", 'name': u"DENOMINATIE", 'label': "denominatie"},
            {'key': u"TELEFOONNUMMER", 'name': u"TELEFOONNUMMER", 'label': "telefoonnummer"},
            {'key': u"INTERNETADRES", 'name': u"INTERNETADRES", 'label': "internetadres"},
            {'key': u"ONDERWIJSSTRUCTUUR", 'name': u"ONDERWIJSSTRUCTUUR", 'label': "onderwijsstructuur"},
            {'key': u"STRAATNAAM CORRESPONDENTIEADRES", 'name': u"STRAATNAAM CORRESPONDENTIEADRES", 'label': "straatnaam_correspondentieadres"},
            {'key': u"HUISNUMMER-TOEVOEGING CORRESPONDENTIEADRES", 'name': u"HUISNUMMER-TOEVOEGING CORRESPONDENTIEADRES", 'label': "huisnummer_toevoeging_correspondentieadres"},
            {'key': u"POSTCODE CORRESPONDENTIEADRES", 'name': u"POSTCODE CORRESPONDENTIEADRES", 'label': "postcode_correspondentieadres"},
            {'key': u"PLAATSNAAM CORRESPONDENTIEADRES", 'name': u"PLAATSNAAM CORRESPONDENTIEADRES", 'label': "plaatsnaam_correspondentieadres"},
            {'key': u"NODAAL GEBIED CODE", 'name': u"NODAAL GEBIED CODE", 'label': "nodaal_gebied_code"},
            {'key': u"NODAAL GEBIED NAAM", 'name': u"NODAAL GEBIED NAAM", 'label': "nodaal_gebied_naam"},
            {'key': u"RPA-GEBIED CODE", 'name': u"RPA-GEBIED CODE", 'label': "rpa_gebied_code"},
            {'key': u"RPA-GEBIED NAAM", 'name': u"RPA-GEBIED NAAM", 'label': "rpa_gebied_naam"},
            {'key': u"WGR-GEBIED CODE", 'name': u"WGR-GEBIED CODE", 'label': "wgr_gebied_code"},
            {'key': u"WGR-GEBIED NAAM", 'name': u"WGR-GEBIED NAAM", 'label': "wgr_gebied_naam"},
            {'key': u"COROPGEBIED CODE", 'name': u"COROPGEBIED CODE", 'label': "coropgebied_code"},
            {'key': u"COROPGEBIED NAAM", 'name': u"COROPGEBIED NAAM", 'label': "coropgebied_naam"},
            {'key': u"ONDERWIJSGEBIED CODE", 'name': u"ONDERWIJSGEBIED CODE", 'label': "onderwijsgebied_code"},
            {'key': u"ONDERWIJSGEBIED NAAM", 'name': u"ONDERWIJSGEBIED NAAM", 'label': "onderwijsgebied_naam"},
            {'key': u"RMC-REGIO CODE", 'name': u"RMC-REGIO CODE", 'label': "rmc_regio_code"},
            {'key': u"RMC-REGIO NAAM", 'name': u"RMC-REGIO NAAM", 'label': "rmc_regio_naam"},
            {'name': u'uni_brin', 'key': u'uni_brin', 'label': u'uni_brin'}
        ]
        self.processed_row = {
            u'brin_nummer': u'18BR',
            u'uni_brin': u'18BR'
        }
        self.processed_row_no_brin = {
            u'gemeentenaam': u'UTRECHT'
        }
        self.bad_filename = "/opt/duo/tests/ocd_backend/test_dumps/badly-formatted.csv"

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

    def test_get_duo_id(self):
        item = self._instantiate_item()
        data = item.get_combined_index_data()
        self.assertEqual(data['id'], self.duo_id)

    def test_get_duo_name(self):
        item = self._instantiate_item()
        data = item.get_combined_index_data()
        self.assertEqual(data['name'], self.duo_name)

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