
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from xml.dom.minidom import parseString
import xpath

__metaclass__ = type
class Weibo:
    def __init__(self, user = None, pwd = None):
        self.qq = 'atupal@foxmail.com' if not user else user
        self.pwd = 'xxxxx' if not pwd else pwd
        self.session = requests.Session()
        self._login()

    def _parse(self, url, _xpath, content = None):
        try:
            if not content:content = self.session.get(url).content
            #doc = xparse.parseDoc(content)
            #ctxt = doc.xpathNewContext()
            #return ctxt.xpathEval(_xpath)
            doc = parseString(content)
            ret = xpath.find(_xpath, doc)
            for i in xrange(len(ret)):
                ret[i].__setattr__('content', ret[i].nodeValue)
            return ret
        except Exception as e:
            print e
            return []
        finally:
            pass

    def _login(self):
        url = 'http://login.weibo.cn/login/'
        ret = self._parse(url, "//*/@href")
        for r in ret:
            print r.content
            print

if __name__ == "__main__":
    W = Weibo()
