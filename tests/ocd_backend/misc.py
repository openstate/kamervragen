import os
from unittest import TestCase
from pprint import pprint

from ocd_backend.utils.unicode_csv import UnicodeReaderAsDict
from ocd_backend.utils.misc import (
    make_hash, make_hash_filename, get_file_id, get_file_encoding, slugify)
from ocd_backend.utils.duo_csv import UnicodeReaderAsSlugs

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

class GetFileEncodingTestCase(TestCase):
    def setUp(self):
        self.filename = "/opt/duo/tests/ocd_backend/test_dumps/65a66c84f4a9a78fcfbf47d4170240ba.csv"
        self.encoding = 'windows-1252'

    def test_get_file_encoding(self):
        encoding = get_file_encoding(self.filename)
        self.assertEqual(encoding['encoding'], self.encoding)

class DuoCSVTestCase(TestCase):
    def setUp(self):
        self.filename = "/opt/duo/tests/ocd_backend/test_dumps/65a66c84f4a9a78fcfbf47d4170240ba.csv"

    def test_header(self):
        with open(self.filename) as csvfile:
            reader = UnicodeReaderAsSlugs(csvfile, delimiter=';')
            # FIXME: this is not ok ;)
            self.header_map = {
                "PROVINCIE":"provincie",
                "BEVOEGD GEZAG NUMMER":"bevoegd gezag nummer",
                "BRIN NUMMER":"brin nummer",
                "INSTELLINGSNAAM":"instellingsnaam",
                "STRAATNAAM":"straatnaam",
                "HUISNUMMER-TOEVOEGING":"huisnummer-toevoeging",
                "POSTCODE":"postcode",
                "PLAATSNAAM":"plaatsnaam",
                "GEMEENTENUMMER":"gemeentenummer",
                "GEMEENTENAAM":"gemeentenaam",
                "DENOMINATIE":"denominatie",
                "TELEFOONNUMMER":"telefoonnummer",
                "INTERNETADRES":"internetadres",
                "ONDERWIJSSTRUCTUUR":"onderwijsstructuur",
                "STRAATNAAM CORRESPONDENTIEADRES":"straatnaam-correspondentieadres",
                "HUISNUMMER-TOEVOEGING CORRESPONDENTIEADRES":"huisnummer-toevoeging-correspondentieadres",
                "POSTCODE CORRESPONDENTIEADRES":"postcode-correspondentieadres",
                "PLAATSNAAM CORRESPONDENTIEADRES":"plaatsnaam-correspondentieadres",
                "NODAAL GEBIED CODE":"nodaal-gebied-code",
                "NODAAL GEBIED NAAM":"nodaal-gebied-naam",
                "RPA-GEBIED CODE":"rpa-gebied-code",
                "RPA-GEBIED NAAM":"rpa-gebied-naam",
                "WGR-GEBIED CODE":"wgr-gebied-code",
                "WGR-GEBIED NAAM":"wgr-gebied-naam",
                "COROPGEBIED CODE":"coropgebied-code",
                "COROPGEBIED NAAM":"coropgebied-naam",
                "ONDERWIJSGEBIED CODE":"onderwijsgebied-code",
                "ONDERWIJSGEBIED NAAM":"onderwijsgebied-naam",
                "RMC-REGIO CODE":"rmc-regio-code",
                "RMC-REGIO NAAM":"rmc-regio-naam"
            }
            self.assertDictEqual(self.header_map, reader.header_map)
