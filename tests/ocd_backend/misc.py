import os
from unittest import TestCase

from ocd_backend.utils.unicode_csv import UnicodeReaderAsDict

class UnicodeReaderAsDictTestCase(TestCase):
    def setUp(self):
        self.PWD = os.path.dirname(__file__)
        self.csv_file = os.path.abspath(os.path.join(self.PWD, 'test_dumps/files.csv'))
        self.csv_encoding = 'utf-8'
        self.first_row = {
            u'bestand': u'https://www.duo.nl/open_onderwijsdata/images/01.-hoofdvestigingen-vo.csv',
            u'pagina': u'https://www.duo.nl/open_onderwijsdata/databestanden/vo/adressen/adressen_vo_1.jsp'
        }

    def test_get_row(self):
        with open(self.csv_file) as csvfile:
            reader = UnicodeReaderAsDict(csvfile)
            row = reader.next()
        self.assertDictEqual(row, self.first_row)
