import os
import json
from pprint import pprint
import re

from ocd_backend.extractors import BaseExtractor, HttpRequestMixin
from ocd_backend.exceptions import ConfigurationError
from ocd_backend.utils.unicode_csv import UnicodeReaderAsDict
from ocd_backend.utils.misc import make_hash_filename, download_file

from ocd_backend import settings


class DownloadExtractor(BaseExtractor, HttpRequestMixin):
    """
    Download files listed in a given CSV file. The extractor only downloads
    files, but does not yield items, as there is no need to store any data.
    """
    def run(self):
        with open(self.source_definition['csv_file']) as csvfile:
            reader = UnicodeReaderAsDict(csvfile)
            for row in reader:
                #pprint(row)
                url = row[self.source_definition['csv_url_field']]
                local_filename = os.path.join(
                    self.source_definition['csv_download_path'],
                    make_hash_filename(url)
                )
                download_file(url, local_filename)
        return []
