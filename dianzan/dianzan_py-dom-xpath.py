# -*- coding=utf-8 -*-

import requests
#import libxml2 as xparse
import sys
#import re
reload(sys)
sys.setdefaultencoding('utf-8')
#import copy

from xml.dom.minidom import parseString
import xpath

__metaclass__ = type
class Dianzan:
    def __init__(self, qq = None, pwd = None):
        self.qq = 'atupal@foxmail.com' if not qq else qq
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
            #doc.freeDoc()
            pass


    def _login(self):
        url = 'http://info50.3g.qq.com/g/s?aid=index&s_it=1&g_from=3gindex&&g_f=1283' #3gqq首页
        url = self._parse(url, '/wml/card/p/a[7]/@href')[0].content  #空间登陆url
        url = self._parse(url, '/wml/card/@ontimer')[0].content  #空间登陆302url
        self.login_referer = url
        data = dict()
        headers = dict()
        content = self.session.get(url).content
        url = self._parse(None, '//*/@href', content = content)[1].content #post地址
        names = ['login_url', 'go_url', 'sidtype', 'aid']
        for name in names:
            value = self._parse(None, '//*[@name="'+ name +'"]/@value', content = content)[0].content
            data[name] = value
        data['qq'] = self.qq
        data['pwd'] = self.pwd
        headers['Origin'] = 'http://pt.3g.qq.com'
        headers['Referer'] = self.login_referer
        headers['Host'] = 'pt.3g.qq.com'
        #headers['User-Agent'] = 'curl/7.21.3 (i686-pc-linux-gnu) libcurl/7.21.3 OpenSSL/0.9.8o zlib/1.2.3.4 libidn/1.18'
        headers['User-Agent'] = ''


        res = self.session.post(url, data = data, headers = headers, allow_redirects = False)
        url = res.headers['location']#post之后重定向的地址，这里如果允许自动跳转的话不知道为什么会跳转到腾讯首页去。。蛋疼

        if not url:
            data = dict()
            img_url = self._parse(None, '//img/@src', content = res.content)[0].content
            names = [
                    'qq'        ,
                    'u_token'   ,
                    'r'         ,
                    'extend'    ,
                    'r_sid'     ,
                    'aid'       ,
                    'hiddenPwd' ,
                    'login_url' ,
                    'go_url'    ,
                    'verify'    ,
                    'sidtype'   ,
                    ]
            for name in names:
                value = self._parse(None, '//*[@name="'+ name +'"]/@value', content = res.content)[0].content
                data[name] = value
            from PIL import Image
            from StringIO import StringIO
            r = self.session.get(img_url)
            verify_img = Image.open(StringIO(r.content))
            verify_img.show()
            import os
            if os.environ['HOME'] == '/home/atupal':
                data['verify'] = raw_input("verify:")
                url = self._parse(None, '//*/@href', content = res.content)[1].content #post地址
                res = self.session.post(url, data = data, headers = headers, allow_redirects = False)
                url = res.headers['location']

                #验证码后第一次get
                url = self._parse(url, '/wml/card/@ontimer')[0].content

                #验证码后第二次get
                url = self._parse(url, '/wml/card/@ontimer')[0].content
        else:
            url = self._parse(url, '/wml/card/@ontimer')[0].content  #再get一次就登陆成功了 ,以上和chrome浏览器都略有不用，没有302

        self.url = url

        #print self.session.get(url).content

        #至此已经登陆成功了

    def dianzan(self, cnt = 5, op = '1'):
        '''
        下面这中方法返回的地址是转义了的。。
        '''
        #patter = r'''<a href="([^>]*?)">赞'''
        #content = self.session.get(self.url).content
        #urls = re.findall(patter, content)

        feed_url = self.url
        url = self._parse(feed_url, '/wml/card/@ontimer') #不知道为什么换了一个qq号的时候这里会多加一个跳转
        if url:
            feed_url = url[0].content
        for i in xrange(cnt):
            print feed_url
            content = self.session.get(feed_url).content

            urls = self._parse(None, '//*/@href', content = content)
            for url in urls:
                if url.content.find('like_action') != -1 and url.content[-1] == op:
                    print self.session.get(url.content).content

            urls = self._parse(None, '//*/@href', content = content)
            for url in urls:
                if url.content.find('feeds_friends') != -1 and url.content.find('dayval=1') != -1:
                    feed_url = url.content




if __name__ == "__main__":
    qq = raw_input('qq:')
    pwd = raw_input('pwd:')
    D = Dianzan(qq = qq, pwd = pwd)
    D.dianzan()
