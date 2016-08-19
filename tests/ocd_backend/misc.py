import os
from unittest import TestCase

from ocd_backend.utils.unicode_csv import UnicodeReaderAsDict
from ocd_backend.utils.misc import make_hash, make_hash_filename, get_file_id

class UnicodeReaderAsDictTestCase(TestCase):
    def setUp(self):
        self.PWD = os.path.dirname(__file__)
        self.csv_file = os.path.abspath(os.path.join(self.PWD, 'test_dumps/files.csv'))
        self.csv_encoding = 'utf-8'
        self.first_row = {
            u'bestand': u'https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv',
            u'pagina': u'https://www.duo.nl/open_onderwijsdata/databestanden/vo/adressen/adressen_vo_1.jsp'
        }
        self.header = [u'bestand', u'pagina']

    def test_get_row(self):
        header = None
        with open(self.csv_file) as csvfile:
            reader = UnicodeReaderAsDict(csvfile)
            row = reader.next()
            header = reader.header
        self.assertEqual(header, self.header)
        self.assertDictEqual(row, self.first_row)


class UrlToFileHashingTestCase(TestCase):
    def setUp(self):
        self.file_url = u'https://www.duo.nl/open_onderwijsdata/databestanden/vo/adressen/adressen_vo_1.jsp'
        self.hash_md5 = u'eb8c1a1798906aa940f7cfc2e86f94f3'
        self.hash_filename = u'eb8c1a1798906aa940f7cfc2e86f94f3.csv'

    def test_make_hash(self):
        print u'blaat'
        hash_md5 = make_hash(self.file_url)
        self.assertEqual(hash_md5, self.hash_md5)

    def test_make_hash_filename(self):
        hash_filename = make_hash_filename(self.file_url)
        self.assertEqual(hash_filename, self.hash_filename)

class FileIdTestCase(TestCase):
    # get_file_id
    def setUp(self):
        self.file_url = u'https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv'
        self.file_id = u'01.-hoofdvestigingen-vo'
        self.percent_url = u'https://www.duo.nl/open_onderwijsdata/images/01.%20Leerlingen%20po%20-%20soort%20po%2C%20cluster%2C%20leeftijd%20-%202015-2016.csv'
        self.percent_id = u'01. Leerlingen po - soort po, cluster, leeftijd - 2015-2016'

    def test_get_file_id(self):
        file_id = get_file_id(self.file_url)
        self.assertEqual(file_id, self.file_id)

    def test_percent_get_file_id(self):
        file_id = get_file_id(self.percent_url)
        self.assertEqual(file_id, self.percent_id)
