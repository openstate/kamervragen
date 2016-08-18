import json
from pprint import pprint
import re

from ocd_backend.extractors import BaseExtractor, HttpRequestMixin
from ocd_backend.exceptions import ConfigurationError
from ocd_backend.utils.unicode_csv import UnicodeReader

from ocd_backend import settings


class DownloadExtractor(BaseExtractor, HttpRequestMixin):
    """
    Download files listed in a given CSV file. The extractor only downloads
    files, but does not yield items, as there is no need to store any data.
    """
    def run(self):
        with open(self.source_definition['csv_file']) as csvfile:
            reader = UnicodeReader(csvfile)
            for row in reader:
                pprint(row)
        return []
