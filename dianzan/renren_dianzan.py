# -*- coding=utf-8 -*-

import requests, requests.utils
import json
import pickle
import logging
from xml.dom.minidom import parseString
import xpath
import re

class RenrenDianzan():
    '''
        self.s: the Session of the object
    '''
    def __init__(self, user = None, pwd = None, debug = False):
        if not user or not pwd:
            with open('./user', 'r') as fi:
                self.user = fi.readline().strip('\n')
                self.pwd = fi.readline().strip('\n')
        else:
            self.user = user
            self.pwd = pwd

        self.session = requests.Session()
        self.debug = debug
        if self._load_cookie():
            self._login()

    def _parse(self, url, _xpath, content = None):
        try:
            if not content:content = self.session.get(url).content
            #doc = xparse.parseDoc(content)
            #ctxt = doc.xpathNewContext()
            #return ctxt.xpathEval(_xpath)
            doc = parseString(content)
            ret = xpath.find(_xpath, doc)
            #for i in xrange(len(ret)):
                #ret[i].__setattr__('content', ret[i].nodeValue)
            return ret
        except Exception as e:
            print e
            return []
        finally:
            #doc.freeDoc()
            pass

    def _load_cookie(self):
        try:
            with open('./renren_login.cookie', 'rb') as fi:
                cookie = pickle.load(fi)
                self.session.cookies.update(cookie)
                return 1
        except Exception as e:
            logging.info(e)
            return 1

    def _login(self):
        self.login_data = {
                'email': self.user,
                'password': self.pwd,
                'autoLogin': "true",
                'icode': '',
                'origURL': 'http://www.renren.com/home',
                'domain': 'renren.com',
                'key_id': '1',
                'captcha_type': 'web_login',
                }
        res = self.session.post('http://renren.com/ajaxLogin/login?1=1&uniqueTimestamp=201350118726', data = self.login_data)
        if self.debug:
            print res.content
        res_json = json.loads(res.content)

        url = res_json['homeUrl'] #回调url
        res = self.session.get(url)

        '''
            保存登录cookie
        '''
        with open('./renren_login.cookie', 'wb') as fi:
            cookie = requests.utils.dict_from_cookiejar(self.session.cookies)
            #pickle.dump(cookie, fi)
        res = re.findall('''ILike_toggleUserLike\((.*?)\)''',res.content )
        '''
            case "blog":
                e = 0;
                break;
            case "album":
                e = 1;
                break;
            case "photo":
                e = 2;
                break;
            case "share":
                e = 3;
                break;
            case "edm":
                e = 4;
                break;
            case "video":
                e = 5;
                break;
            case "status":
                e = 6
        '''
        type_id = {
                'blog':'0',
                'album': '1',
                'photo': '2',
                'share': '3',
                'edm': '4',
                'video': '5',
                'status': '6',
                }
        for  r in res:
            import random
            r= r.replace("'", '').split(',')
            url = ('http://like.renren.com/addlike?' +
            'gid='+r[0] + '_' + r[1] +
            '&uid=%s' % r[2] +
            '&owner=%s' % r[3]+
            '&type='+ type_id[r[0]]  +
            '&name=%E4%BD%99%E5%BA%B7%E4%B9%90.py'+
            '&t=' + str(random.random))
            headers = {
                    'Referer':'http://like.renren.com/ajaxproxy.htm',
                    'Host': 'like.renren.com',
                    }
            print self.session.get(url, headers = headers).content



    def dianzan(self):
        pass


if __name__ == "__main__":
    R = RenrenDianzan(debug = True)
