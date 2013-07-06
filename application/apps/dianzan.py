#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  author : atupal
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  site: http://atupal.org

import requests #import libxml2 as xparse import sys #import re reload(sys) sys.setdefaultencoding('utf-8') #import copy

from xml.dom.minidom import parseString
import xpath
import lxml.html
#from pprint import pprint as printf
import urllib
import logging
import unittest

try:
    from application.apps.db_methods import init_db
    from application.apps.db_methods import add_task
except:
    from db_methods import init_db
    from db_methods import add_task


__metaclass__ = type
class Dianzan:
    '''
        qq         : qq帐号, 邮箱格式数字格式均可
        pwd        : 密码, 测试帐号和密码是保存在当前目录下的user文集中
        feq        : 点赞次数
        inc        : 点赞的时间增量(即间隔)
        cnt        : 点赞的页数
        session    : 保存了用户cookie的session对象(requests.Session)
        repeat_set : 由于空间存在一些无法点赞或者没有权限点赞的content, 所以加个hash表判断下
        url        : 用户的主feed页面(带书签)
        frr        : 只点赞某些用户, 如果为空就全部点赞
        pos        : 出现了这些词语就点赞, 如果和neg重复了, 优先点赞
        neg        : 出现了这些词语就不点赞
    '''

    def __init__(self, qq = None, pwd = None, feq = 1, inc = 10, cnt = 1, url = None, frr = '', pos = '', neg = ''):
        self.qq = 'atupal@foxmail.com' if not qq else qq
        self.pwd = 'xxxxx' if not pwd else pwd
        self.feq = feq
        self.inc = inc
        self.cnt = cnt
        self.session = requests.Session()
        self._login()
        self.repeat_set = set()

    def _parse(self, url, _xpath, content = None):
        '''
            由content或者url  以及相应的xpath的返回结果
        '''

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

    def lxml_parse(self, url, _xpath, content = None):
        try:
            if not content: content = self.session.get(url).content
            ret = lxml.html.fromstring(content).xpath(_xpath)
            return ret
        except Exception as e:
            logging.error('lxml_parse:' + str(e))
            return None


    def _login(self):
        '''
            空间登录, 获取用户的一个书签, 指向的是主feed页面, 保存为self.url
        '''

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
            '''
                碰到需要验证码的情况了, 一般是第一次登录的ip会需要, 再者是异常的ip, 比如登录了很多个qq的sae服务器
            '''
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
                    #'verify'    ,
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
            url = self._parse(None, '//*/@href', content = res.content)[1].content #post地址
            import os
            if os.environ.get('HOME') == '/home/atupal':
                data['verify'] = raw_input("verify:")
                url = self._verify(data = data, headers = headers, url = url)

            else:
                form = '<form action="/dianzan_verify" method="post">'
                for i in data:
                    form += '<input type="hidden" name="%s" value="%s"></input>'%(i, data[i])

                form += '<input type="hidden" name="url" value="%s"></input>'%url #带上url，下次浏览器post接收
                form += '<input type="text" name="verify"></input>'
                form += '<input type="submit" value="confirm"></input>'
                form += '</form>'
                self.verify = '''
                    <html>
                        <img src="%s"/>
                        %s
                    </html>
                '''%(img_url, form)

                return

        else:
            url = self._parse(url, '/wml/card/@ontimer')[0].content  #再get一次就登陆成功了 ,以上和chrome浏览器都略有不用，没有302

        self.verify = None
        self.url = url

        feed_url = self.url
        url = self._parse(feed_url, '/wml/card/@ontimer') #不知道为什么换了一个qq号的时候这里会多加一个跳转
        if url:
            feed_url = url[0].content

        self.url = feed_url


        #至此已经登陆成功了

    def _verify(self, data, headers, url = None):
        '''
            提交验证码,完成登录步骤
        '''

        if not url:
            url = data.pop('url')
            self.url = url  # Dianzan_verify子类没有登录, 所以手动添加url 属性
        res = self.session.post(url, data = data, headers = headers, allow_redirects = False)
        print '1' + str(res.content)
        url = res.headers['location']

        #验证码后第一次get
        content = self.session.get(url).content
        print '2' + content
        url = self._parse(None, '/wml/card/@ontimer', content = content)[0].content

        #验证码后第二次get
        content = self.session.get(url).content
        print '3' + content

        #有的账号会再跳转一次，有的不会,算个bug吧
        try:
            url_tmp = self._parse(None, '/wml/card/@ontimer', content = content)[0].content
        except:
            url_tmp = None
        if url_tmp:
            url = url_tmp

        return self.url

    def get_zan_datail(self, content):
        '''
            获取说说的uid和content以及url
            ret: 生成器, 元素为一个三元tuple: ( url, content, uid )
        '''
        xparser = lxml.html.fromstring(content)
        filt = lambda x:x.values() and x.values()[0].find('like_action') != -1 and x.values()[0][-1] == '0'
        urls = filter(filt, xparser.xpath('//a') )


        for url in urls:
            try:zan_url = url.values()[0]
            except:zan_url = ''
            try:
                html_ele = url.getnext().getnext().values()[0]
            except:
                html_ele = ''

            ind = html_ele.find('mood_con=') + len('mood_con=')
            zan_content = urllib.unquote(html_ele[ind:])

            ind_begin = html_ele.find('mood_uin=') + len('mood_uin=')
            ind_end = html_ele.find('&mood_id')

            zan_uid = html_ele[ind_begin:ind_end]

            yield zan_url, zan_content, zan_uid

    def get_friend(self):
        '''
            获取好友列表, 默认是全部点赞的, 设置为只对某些好友点赞后就得获取好友列表了
        '''
        #string = '好友'.decode('utf-8').encode('ascii', 'xmlcharrefreplace')
        url_ele = self.lxml_parse(url = self.url, _xpath = '//a[text()="%s"]' % u'好友')
        try:
            friend = {}
            url = url_ele[0].values()[0]
            all_friend_url = self.lxml_parse(url, _xpath = '//a[text()="%s"]' % u'全部' )[0].values()[0]
            cnt = 0
            while all_friend_url:
                cnt += 1
                content = self.session.get(all_friend_url).content
                urls = self.lxml_parse(url = None, _xpath = '//a' ,content = content)
                for url in urls:
                    tmp = url
                    url = url.values()[0]
                    '''
                    http://blog60.z.qq.com/blog.jsp?B_UID=158839520&amp;sid=AR8VO35GzIJG_OWjm9obXweE
                    '''
                    if url.startswith('http://blog60.z.qq.com/blog.jsp?') and url.find("B_UID") != -1 and url.count('&') == 1:
                        begin = url.find('B_UID=') + len('B_UID=')
                        end = url.find('&sid')
                        if tmp.text != u'主页':
                            friend[url[begin:end]] = tmp.text

                try:all_friend_url = self.lxml_parse(url = None, content = content, _xpath = '//a[text()="%s"]' % u'下页' )[0].values()[0]
                except IndexError:all_friend_url = []
                except Exception as e:logging.error("next_page:" + str(e));all_friend_url=[]

            return friend

        except Exception as e:
            return {}
            logging.error('get_griend' + str(e))


    def dianzan(self, cnt = 5, op = '1', url_from_db = None):
        '''
        下面这中方法返回的地址是转义了的。。
        '''
        #patter = r'''<a href="([^>]*?)">赞'''
        #content = self.session.get(self.url).content
        #urls = re.findall(patter, content)

        if self.verify:
            return self.verify

        if not url_from_db:feed_url = self.url
        else: feed_url = url_from_db
        #url = self._parse(feed_url, '/wml/card/@ontimer') #不知道为什么换了一个qq号的时候这里会多加一个跳转
        #if url:
        #    feed_url = url[0].content

        #self.url = feed_url

        for i in xrange(cnt):
            print "feed_url:" + feed_url
            content = self.session.get(feed_url).content

            urls = self._parse(None, '//*/@href', content = content)
            import json
            return json.dumps( self.get_friend() )


            for url in urls:
                if url.content.find('like_action') != -1 and url.content[-1] == op:
                    if self.repeat_set.issuperset({url.content}):
                        continue
                    ret = self.session.get(url.content).content
                    if ret.find('成功') != -1:
                        print '赞成功'
                    self.repeat_set.add(url.content)

            urls = self._parse(None, '//*[text()="更多好友动态>>" or text()="下页"]/@href', content = content)
            for url in urls:
                #if url.content.find('feeds_friends') != -1 or url.content.find('dayval=1') != -1:
                feed_url = url.content

        return 'success'


    def add_tast(self):
        '''
            添加 任务
        '''

        pass

class Dianzan_verify(Dianzan):
    def __init__(self):
        '''
            覆盖掉父类的构造方法, 防止执行父类构造方法中的_login函数
        '''
        self.session = requests.Session()

    def verify(self, data, headers):
        print data
        self.url = self._verify(data = data, headers = headers)
        self.verify = None


class Dianzan_from_url(Dianzan):
    def __init__(self):
        '''
            覆盖掉父类的构造方法, 防止执行父类构造方法中的_login函数
        '''
        self.verify = None
        self.session = requests
        pass


class DianzanTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _test_db(self):
        db = init_db()
        add_task(db, uid = 'ts', url = 'ts')

    def _test_dianzan(self):
        #qq = raw_input('qq:')
        #pwd = raw_input('pwd:')
        qq = 'atupal@qq.com'
        pwd = 'atupal@qq.com'
        D = Dianzan(qq = qq, pwd = pwd)
        D.dianzan(cnt = 1)


if __name__ == "__main__":
    unittest.main()
