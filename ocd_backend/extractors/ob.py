import copy
import json
from pprint import pprint

from ocd_backend.extractors import BaseExtractor
from ocd_backend.exceptions import ConfigurationError

import feedparser


class OBExtrator(BaseExtractor):
    def __init__(self, *args, **kwargs):
        super(OBExtrator, self).__init__(*args, **kwargs)

        if 'feed_url' not in self.source_definition:
            raise ConfigurationError('Missing \'feed_url\' definition')

        if not self.source_definition['feed_url']:
            raise ConfigurationError('The \'feed_url\' is empty')

        self.feed_url = self.source_definition['feed_url']

    def extract_items(self, feed):
        """Parses the static content and extracts the items."""

        for entry in feed.entries:
            doc = {}
            for key in self.source_definition.get("feed_keys", entry.keys()):
                doc[key] = getattr(entry, key)
            pprint(doc)
            yield 'application/json', json.dumps(doc)

    def run(self):
        feed = feedparser.parse(self.feed_url)

        # Extract and yield the items
        for item in self.extract_items(feed):
            yield item
