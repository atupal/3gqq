# -*- coding=utf-8 -*-

import requests
import json

class RenrenDianzan():
    '''
        self.s: the Session of the object
    '''
    def __init__(self, user = None, pwd = None, debug = False):
        self.user = user if user else "atupal@foxmail.com"
        self.pwd = pwd if pwd else "LKYs4690102"
        self.s = requests.Session()
        self.debug = debug
        self._login()

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
        res = self.s.post('http://renren.com/ajaxLogin/login?1=1&uniqueTimestamp=201350118726', data = self.login_data)
        if self.debug:
            print res.content
        res_json = json.loads(res.content)

        url = res_json['homeUrl'] #回调url
        res = self.s.get(url)
        if self.debug:
            print res.content


if __name__ == "__main__":
    R = RenrenDianzan(debug = True)
