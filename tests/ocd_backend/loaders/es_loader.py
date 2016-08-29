import json
import os.path

from . import LoaderTestCase
from ocd_backend.exceptions import ConfigurationError
from ocd_backend.loaders import ElasticsearchLoader


class ESLoaderTestCase(LoaderTestCase):
    def setUp(self):
        super(ESLoaderTestCase, self).setUp()
        self.PWD = os.path.dirname(__file__)
        self.object_id = u'52c54e5be11b218b1a6df731634fda9fb2188d57'

        with open(os.path.join(self.PWD, '../test_dumps/combined_index_doc.json'), 'r') as f:
            self.combined_index_doc = json.load(f)

        with open(os.path.join(self.PWD, '../test_dumps/index_doc.json'), 'r') as f:
            self.index_doc = json.load(f)

        dump_path = os.path.abspath(os.path.join(self.PWD, '../test_dumps/ocd_openbeelden_test.gz'))

        self.source_definition = {
            'id': 'test_definition',
            'extractor': 'ocd_backend.extractors.staticfile.StaticJSONDumpExtractor',
            'transformer': 'ocd_backend.transformers.BaseTransformer',
            'item': 'ocd_backend.items.LocalDumpItem',
            'loader': 'ocd_backend.loaders.ElasticsearchLoader',
            'alt_doc_type': '01.-hoofdvestigingen-vo',
            'dump_path': dump_path
        }
        self.loader = ElasticsearchLoader()

        self.doc_type_default = 'items'
        self.doc_type = '01_hoofdvestigingen_vo'

    def test_throws_configuration_error_without_index_name(self):
        # self.loader.run(source_definition=self.source_definition)
        self.assertRaises(ConfigurationError, self.loader.run,
                          source_definition=self.source_definition)

    def test_get_doc_type(self):
        """Tests getting the doc_type from the source config. It can be a name
        or a reference to a field of an object."""
        result = self.loader._get_doc_type(self.source_definition, 'items')
        self.assertEqual(result, self.doc_type_default)
        result = self.loader._get_doc_type(self.source_definition, '@alt_doc_type')
        self.assertEqual(result, self.doc_type)
