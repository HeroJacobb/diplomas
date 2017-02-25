import pycurl
from StringIO import StringIO

class Curl:
    def __init__(self,host):
        self.url=str(host)

    def get_page(self,file=None):
        try:
            buffer = StringIO()
            c = pycurl.Curl()
            c.setopt(c.URL, self.url)
            c.setopt(c.WRITEDATA, buffer)
            c.perform()
            c.close()
            body = buffer.getvalue()
            #print body
            try:
               open(file, 'w').write(body)
            except:
                None#ds

            return body
        except (pycurl.error):
            print "Error"



