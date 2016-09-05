import re

from .unicode_csv import UnicodeReaderAsDict
from .misc import slugify, get_file_encoding

class UnicodeReaderAsSlugs(UnicodeReaderAsDict):
    def __init__(self, f, dialect='excel', encoding="utf-8", **kwds):
        super(UnicodeReaderAsSlugs, self).__init__(f, dialect, encoding, **kwds)
        self.header_map = {unicode(h.strip()): unicode(slugify(h.strip(), '_')) for h in self.header}
        self.num_columns = len(self.header)

    def next(self):
        row = super(UnicodeReaderAsSlugs, self).next()

        if len(row.keys()) != self.num_columns:
            raise ValueError("The number of values in this row does not match the number of headers")

        return {self.header_map[k.strip()]: v for k,v in row.iteritems()}


def check_csv(local_filename):
    # encoding = get_file_encoding(self.original_item['local_filename'])['encoding']
    encoding= 'iso-8859-1'
    with open(local_filename) as csvfile:
        try:
            reader = UnicodeReaderAsSlugs(csvfile, delimiter=';', encoding=encoding)
        except Exception as e:
            return False
        try:
            while True:
                try:
                    row = reader.next()
                except StopIteration as e:
                    break
        except ValueError as e:
            return False
    return True
