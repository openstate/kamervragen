import json
from pprint import pprint

from unittest import TestCase

from ocd_backend.loaders import ElasticsearchWithRedisDataLoader

class DuoLoaderTestCase(TestCase):
    def setUp(self):
        super(DuoLoaderTestCase, self).setUp()

        self.loader = ElasticsearchWithRedisDataLoader()

        self.loader.source_definition = {
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
            "csv_download_path": "/opt/duo/tests/ocd_backend/test_dumps",
            "fields_mapping": {
                "uni_brin": ["brin_nummer", "brin_code"]
            }
        }

        self.original_object_urls = {
            u'html': u'https://www.duo.nl/open_onderwijsdata/databestanden/vo/adressen/adressen_vo_1.jsp',
            u'csv': u'https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv'
        }

        self.duo_id = u'01.-hoofdvestigingen-vo'
        self.duo_name = u'01.-hoofdvestigingen-vo'

        self.header_map = {
            u"PROVINCIE": "provincie",
            u"BEVOEGD GEZAG NUMMER": "bevoegd_gezag_nummer",
            u"BRIN NUMMER": "brin_nummer",
            u"INSTELLINGSNAAM": "instellingsnaam",
            u"STRAATNAAM": "straatnaam"
        }

        self.processed_field_definitions = [
            {'key': u"PROVINCIE", 'name': u"PROVINCIE", 'label': "provincie"},
            {'key': u"BEVOEGD GEZAG NUMMER", 'name': u"BEVOEGD GEZAG NUMMER", 'label': "bevoegd_gezag_nummer"},
            {'key': u"BRIN NUMMER", 'name': u"BRIN NUMMER", 'label': "brin_nummer"},
            {'key': u"INSTELLINGSNAAM", 'name': u"INSTELLINGSNAAM", 'label': "instellingsnaam"},
            {'key': u"STRAATNAAM", 'name': u"STRAATNAAM", 'label': "straatnaam"},
            {'name': u'uni_brin', 'key': u'uni_brin', 'label': u'uni_brin'}
        ]

        self.processed_field_definitions_no_uni_brin = [
            {'key': u"PROVINCIE", 'name': u"PROVINCIE", 'label': "provincie"},
            {'key': u"BEVOEGD GEZAG NUMMER", 'name': u"BEVOEGD GEZAG NUMMER", 'label': "bevoegd_gezag_nummer"},
            {'key': u"INSTELLINGSNAAM", 'name': u"INSTELLINGSNAAM", 'label': "instellingsnaam"},
            {'key': u"STRAATNAAM", 'name': u"STRAATNAAM", 'label': "straatnaam"}
        ]

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

        self.loader.new_index_names = ['duo_data_items_testje']

        self.processed_row = {
            u'@row': 1,
            u'brin_nummer': u'18BR',
            u'uni_brin': u'18BR'
        }
        self.processed_row_no_brin = {
            u'@row': 1,
            u'gemeentenaam': u'UTRECHT'
        }
        self.bad_filename = "/opt/duo/tests/ocd_backend/test_dumps/badly-formatted.csv"

    def test_get_data(self):
        fields, data = self.loader._get_data(self.original_object_urls[u'csv'], self.duo_id)
        self.assertListEqual(
            sorted(fields, key=lambda x: x['key']),
            sorted(self.fields, key=lambda x: x['key']))

    def test_process_row(self):
        processed_row = self.loader._process_row(
            self.duo_id, {u'brin_nummer': u'18BR'}, 1, self.loader.new_index_names[0])
        pprint(processed_row)
        self.assertDictEqual(processed_row[0]['_source'], self.processed_row)
        processed_row_no_brin = self.loader._process_row(
            self.duo_id, {u'gemeentenaam': u'UTRECHT'}, 1, self.loader.new_index_names[0])
        self.assertDictEqual(processed_row_no_brin[0]['_source'], self.processed_row_no_brin)

    def test_get_field_definitions(self):
        result = self.loader._get_field_definitions(
            self.header_map, self.loader.source_definition["fields_mapping"])
        self.assertEqual(
            sorted(result, key=lambda x: x['key']),
            sorted(self.processed_field_definitions, key=lambda x: x['key']))

    def test_get_field_definitions_no_uni_brin(self):
        del self.header_map[u"BRIN NUMMER"]
        result = self.loader._get_field_definitions(
            self.header_map, self.loader.source_definition["fields_mapping"])
        self.assertEqual(
            sorted(result, key=lambda x: x['key']),
            sorted(self.processed_field_definitions_no_uni_brin, key=lambda x: x['key']))


    # def test_get_data_lookup_error(self):
    #     del self.item['local_filename']
    #     item = self._instantiate_item()
    #     with self.assertRaises(LookupError):
    #         fields, data = item._get_data()
    #
    # def test_get_data_value_error(self):
    #     self.item['local_filename'] = self.bad_filename
    #     item = self._instantiate_item()
    #     with self.assertRaises(ValueError):
    #         fields, data = item._get_data()
