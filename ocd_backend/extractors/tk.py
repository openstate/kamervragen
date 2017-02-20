import json
from pprint import pprint

import redis

from ocd_backend.extractors.staticfile import StaticJSONExtractor


class TweedeKamerExtractor(StaticJSONExtractor):
    redis_client = None

    def _get_feed_url(self, url):
        return self.http_session.get(
            url, headers={
                'Authorization': (
                    'Basic dG9ta3VuemxlcjpEUk4kTyRrelF4NUVaaCVsem03YQ==')
            }, verify=False)

    def extract_items(self, static_content):
        # TODO: implement piket paaltjes stuff ....
        page_number = 1
        static_json = static_content
        while static_json:
            print "Processing page number %s ..." % (page_number,)

            for item in static_json['entries']:
                yield 'application/json', json.dumps(item)

            next_links = [
                l for l in static_json['links'] if l['rel'] == 'next']
            static_json = None
            if len(next_links) > 0:
                result = self._get_feed_url(next_links[0]['href'])
                if result.status_code >= 200 and result.status_code < 300:
                    page_number += 1
                    self.redis_client.set(
                        'tk_piketpaaltje_url', next_links[0]['href'])
                    static_json = result.json()
                else:
                    print "Get status code : %s" % (result.status_code,)

    def run(self):
        # Retrieve the static content from the source
        # TODO: disable ssl verification fro now since the
        # almanak implementation (of ssl) is broken.

        self.redis_client = redis.StrictRedis()

        piket_url = self.redis_client.get('tk_piketpaaltje_url')
        if not piket_url:
            piket_url = self.file_url
        else:
            print "Got piketpaaltje, skipping to the last URL:"
        print piket_url
        r = self._get_feed_url(piket_url)
        r.raise_for_status()

        static_content = r.json()

        # Extract and yield the items
        for item in self.extract_items(static_content):
            yield item
