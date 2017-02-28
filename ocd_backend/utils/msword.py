import tempfile
from urllib2 import HTTPError
from subprocess import Popen, PIPE

from OpenSSL.SSL import ZeroReturnError

from magic import Magic

import docx

m = Magic(mime=True)


def get_text(filename):
    try:
        doc = docx.Document(filename)
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        return '\n'.join(fullText)
    except Exception:
        cmd = ['antiword', filename]
        p = Popen(cmd, stdout=PIPE)
        stdout, stderr = p.communicate()
        return stdout.decode('ascii', 'ignore')


class WordToTextMixin(object):
    """
    Interface for converting a Word file into text format using python docx
    """

    def word_clean_text(self, text):
        return text
        # return re.sub(r'\s+', u' ', text)

    def word_get_contents(self, url, max_pages=20):
        """
        Convenience method to download a Word file and converting it to text.
        """
        tf = self.word_download(url)
        if tf is not None:
            print "Download went ok, now trying to convert ..."
            try:
                result = self.word_to_text(tf.name, max_pages)
                print "Conversion was ok ..."
            except Exception as e:
                print "Conversion was not ok ..."
                print e
                t = m.from_file(tf.name)
                print t
                result = u''
            return result
        else:
            print "Download did not go ok ..."
            return u''  # FIXME: should be something else ...

    def word_download(self, url):
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
        except HTTPError as e:
            print "Something went wrong downloading %s" % (url,)
        except ZeroReturnError as e:
            print "SSL Zero return error %s" % (url,)
        except Exception as e:
            print "Some other exception %s" % (url,)

    def word_to_text(self, path, max_pages=20):
        """
        Method to convert a given Word file into text file using python docx
        """
        return get_text(path)
