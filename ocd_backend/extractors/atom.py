from lxml import etree
import json

from ocd_backend.extractors.staticfile import StaticXmlExtractor


class AtomExtractor(StaticXmlExtractor):
    def extract_items(self, static_content):
        page_number = 1
        while static_content:
            print "Processing page number %s ..." % (page_number,)
            tree = etree.fromstring(static_content)

            self.namespaces = None
            if self.default_namespace is not None:
                # the namespace map has a key None if there is a default
                # namespace so the configuration has to specify the default key
                # xpath queries do not allow an empty default namespace
                self.namespaces = tree.nsmap
                try:
                    self.namespaces[self.default_namespace] = self.namespaces[
                        None]
                    del self.namespaces[None]
                except KeyError:
                    pass

            for item in tree.xpath(
                    self.item_xpath, namespaces=self.namespaces):
                print etree.tostring(item)
                print "---"
                yield 'application/xml', etree.tostring(item)
                # yield 'application/json', json.dumps({
                #     'id': u''.join(item.xpath('.//atom:id//text()', namespaces=self.namespaces))
                # })
            next_page = tree.xpath(
                '//atom:feed/atom:link[@rel="next"]/@href',
                namespaces=self.namespaces)
            static_content = None
            if len(next_page) > 0:
                result = self.http_session.get(next_page[0], verify=False)
                if result.status_code >= 200 and result.status_code < 300:
                    page_number += 1
                    static_content = result.content
