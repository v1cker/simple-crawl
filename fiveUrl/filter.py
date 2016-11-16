# Refer -> http://stackoverflow.com/questions/12553117/how-to-filter-duplicate-requests-based-on-url-in-scrapy
from scrapy.dupefilters import RFPDupeFilter
from scrapy.utils.request import request_fingerprint
from urlparse import urlparse
import re

class CustomFilter(RFPDupeFilter):
    def __init__(self,path=None,debug=None):
        RFPDupeFilter.__init__(self,path,debug)
        self.fingerprints = {}

    def __getid(self,url):
        mm = urlparse(url)[1]
        return mm

    def request_seen(self, request):
        fp = self.__getid(request.url)
        if 'sdu.edu.cn' not in request.url and not re.match('http://\d+\.\d+\.\d+\.\d+',request.url):
            return True
        if not self.fingerprints.has_key(fp):
            self.fingerprints[fp]=0
            return False
        else:
            if self.fingerprints[fp]:
                self.fingerprints[fp]+=1
                return False
            else:
                return True
