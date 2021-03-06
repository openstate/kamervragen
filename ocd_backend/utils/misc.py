import datetime
import json
import re
import hashlib
import urllib2

import translitcodec
import requests
from chardet.universaldetector import UniversalDetector

from elasticsearch.helpers import scan, bulk


def reindex(client, source_index, target_index, target_client=None, chunk_size=500, scroll='5m', transformation_callable=None):
    """
    Reindex all documents from one index to another, potentially (if
    `target_client` is specified) on a different cluster.

    .. note::

        This helper doesn't transfer mappings, just the data.

    :arg client: instance of :class:`~elasticsearch.Elasticsearch` to use (for
        read if `target_client` is specified as well)
    :arg source_index: index (or list of indices) to read documents from
    :arg target_index: name of the index in the target cluster to populate
    :arg target_client: optional, is specified will be used for writing (thus
        enabling reindex between clusters)
    :arg chunk_size: number of docs in one chunk sent to es (default: 500)
    :arg scroll: Specify how long a consistent view of the index should be
        maintained for scrolled search
    """
    target_client = client if target_client is None else target_client

    docs = scan(client, index=source_index, scroll=scroll, _source_include=['*'])
    def _change_doc_index(hits, index):
        for h in hits:
            h['_index'] = index
            if transformation_callable is not None:
                h = transformation_callable(h)
            yield h

    return bulk(target_client, _change_doc_index(docs, target_index),
        chunk_size=chunk_size, stats_only=True)


def load_sources_config(filename):
    """Loads a JSON file containing the configuration of the available
    sources.

    :param filename: the filename of the JSON file.
    :type filename: str.
    """
    if type(filename) == file:
        # Already an open file
        return json.load(filename)
    try:
        with open(filename) as json_file:
            return json.load(json_file)
    except IOError, e:
        e.strerror = 'Unable to load sources configuration file (%s)' % (
            e.strerror,)
        raise


def load_object(path):
    """Load an object given it's absolute object path, and return it.

    The object can be a class, function, variable or instance.

    :param path: absolute object path (i.e. 'ocd_backend.extractor.BaseExtractor')
    :type path: str.
    """
    try:
        dot = path.rindex('.')
    except ValueError:
        raise ValueError, "Error loading object '%s': not a full path" % path

    module, name = path[:dot], path[dot+1:]
    try:
        mod = __import__(module, {}, {}, [''])
    except ImportError, e:
        raise ImportError, "Error loading object '%s': %s" % (path, e)

    try:
        obj = getattr(mod, name)
    except AttributeError:
        raise NameError, "Module '%s' doesn't define any object named '%s'" % (
            module, name)

    return obj


def try_convert(conv, value):
    try:
        return conv(value)
    except ValueError:
        return value


def parse_date(regexen, date_str):
    """
        Parse a messy string into a granular date

        `regexen` is of the form [ (regex, (granularity, groups -> datetime)) ]
    """
    if date_str:
        for reg, (gran, dater) in regexen:
            m = re.match(reg, date_str)
            if m:
                try:
                    return gran, dater(m.groups())
                except ValueError:
                    return 0, None
    return 0, None


def parse_date_span(regexen, date1_str, date2_str):
    """
        Parse a start & end date into a (less) granular date

        `regexen` is of the form [ (regex, (granularity, groups -> datetime)) ]
    """
    date1_gran, date1 = parse_date(regexen, date1_str)
    date2_gran, date2 = parse_date(regexen, date2_str)

    if date2:
        # TODO: integrate both granularities
        if (date1_gran, date1) == (date2_gran, date2):
            return date1_gran, date1
        if (date2 - date1).days < 5*365:
            return 4, date1
        if (date2 - date1).days < 50*365:
            return 3, date1
        if (date2 - date1).days >= 50*365:
            return 2, date1
    else:
        return date1_gran, date1


class DatetimeJSONEncoder(json.JSONEncoder):
    """
    JSONEncoder that can handle ``datetime.datetime``, ``datetime.date`` and
    ``datetime.timedelta`` objects.
    """
    def default(self, o):
        if isinstance(o, datetime.datetime) or isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, datetime.timedelta):
            return (datetime.datetime.min + o).time().isoformat()
        else:
            return super(DatetimeJSONEncoder, self).default(o)

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = word.encode('translit/long')
        if word:
            result.append(word)
    return unicode(delim.join(result))

def make_hash(contents):
    m = hashlib.md5()
    m.update(contents)
    return m.hexdigest()

def make_hash_filename(url, extension='.csv'):
    return u'%s%s' % (make_hash(url), extension,)

def download_file(url, local_filename):
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

def get_file_id(url):
    return urllib2.unquote(url).rsplit('/')[-1].replace('.csv', '')

def get_file_encoding(filename):
    detector = UniversalDetector()
    for line in file(filename, 'rb'):
        detector.feed(line)
        if detector.done: break
    detector.close()
    return detector.result
