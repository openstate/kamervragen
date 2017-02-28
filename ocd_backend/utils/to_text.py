import tempfile
from urllib2 import HTTPError

from OpenSSL.SSL import ZeroReturnError

from magic import Magic

from ocd_backend.utils.pdf import PDFToTextMixin
from ocd_backend.utils.msword import WordToTextMixin

m = Magic(mime=True)


class FileToTextMixin(PDFToTextMixin, WordToTextMixin):
    """
    Interface for converting a file into text format
    """

    def text_download(self, url):
        """
        Downloads a given url to a tempfile.
        """

        print "Downloading %s" % (url,)
        try:
            # GO has no wildcard domain for SSL
            r = self.http_session.get(url, verify=False)
            tf = tempfile.NamedTemporaryFile()
            tf.write(r.content)
            tf.seek(0)
            return tf
        except HTTPError:
            print "Something went wrong downloading %s" % (url,)
        except ZeroReturnError:
            print "SSL Zero return error %s" % (url,)
        except Exception:
            print "Some other exception %s" % (url,)

    def text_get_contents(self, url, max_pages=20):
        tf = self.word_download(url)
        if tf is None:
            return u''

        mime_type = m.from_file(tf.name)

        if mime_type in [
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/msword'
        ]:
            return self.word_to_text(tf.name, max_pages)
        else:
            return self.pdf_to_text(tf.name, max_pages)
