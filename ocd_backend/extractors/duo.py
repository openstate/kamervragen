import os
import json
from pprint import pprint
import re

from ocd_backend.extractors import BaseExtractor, HttpRequestMixin
from ocd_backend.exceptions import ConfigurationError
from ocd_backend.utils.unicode_csv import UnicodeReaderAsDict
from ocd_backend.utils.misc import make_hash_filename, download_file

from ocd_backend import settings


class CSVExtractor(BaseExtractor):
    """
    Add a mathod to read a CSV file. Yields rows as dicts.
    """
    def _read(self):
        with open(self.source_definition['csv_file']) as csvfile:
            reader = UnicodeReaderAsDict(csvfile)
            for row in reader:
                yield row


class DownloadExtractor(CSVExtractor):
    """
    Download files listed in a given CSV file. The extractor only downloads
    files, but does not yield items, as there is no need to store any data.
    """
    def run(self):
        for row in self._read():
            url = row[self.source_definition['csv_url_field']]
            print url
            local_filename = os.path.join(
                self.source_definition['csv_download_path'],
                make_hash_filename(url)
            )
            # FIXME: does not actually use the request mixin right now
            download_file(url, local_filename)
        return []


class DUOCSVListExtractor(CSVExtractor):
    """
    Loops through the given CSV files and yields items for further ETL
    processing.
    """
    def run(self):
        for row in self._read():
            url = row[self.source_definition['csv_url_field']]
            local_filename = os.path.join(
                self.source_definition['csv_download_path'],
                make_hash_filename(url)
            )
            record = {
                'file': url,
                'page': row[self.source_definition['csv_page_field']],
                'local_filename': local_filename
            }

            # only yield items if we have the download ....
            if os.path.exists(local_filename):
                yield 'application/json', json.dumps(record)
