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
