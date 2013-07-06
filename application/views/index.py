#-*- coding=utf-8 -*-

from application import app
from flask import request
from flask import render_template

from application.apps import dianzan
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from application.apps.db_methods import init_db
from application.apps.db_methods import add_task
import logging
import traceback


@app.route('/')
def index():
    return render_template('index.html')

#import logging
@app.route('/dianzan', methods = ['POST'])
def _dianzan():
    if request.method != 'POST':
        return 'methods not allowed!'
    try:
        qq = request.form.get('qq', '')
        pwd = request.form.get('pwd', '')
        cnt = request.form.get('cnt', '1')
        feq = request.form.get('feq', '10')  # 点赞次数
        inc = request.form.get('inc', '10')
        frr = request.form.get('frr', '')
        pos = request.form.get('pos', '')
        neg = request.form.get('neg', '')

        try:D = dianzan.Dianzan(qq = qq, pwd = pwd, cnt = int(cnt), feq = int(feq), inc = int(inc))
        except Exception as e: print e

        if str(frr) == "on":
            return 'coding , please wait'

        ret = D.dianzan(cnt = int(cnt))

        try:
            feq = int(feq)
            inc = int(inc)

            if (feq * inc - inc) > 0:
                db = init_db()
                add_task(db, uid = D.qq, url = D.url, ttl = feq * inc - inc, inc = inc, pos = pos, neg = neg)
        except Exception as e:
            logging.error('/dianzan:' + str(e))
            traceback.print_exc(file=sys.stdout)

    except Exception as e:
        #logging.error(str(e))
        print str(e)
        ret = str(e)
        ret += "<hr/>"
        ret += "<p>%s</p>"%("用户名，密码错误，请再试一次")
    return ret

@app.route('/dianzan_verify', methods = ['POST'])
def _dianzan_verify():
    if request.method != 'POST':
        return 'methods not allowed!'
    headers = dict()
    headers['Origin'] = 'http://pt.3g.qq.com'
    headers['Host'] = 'pt.3g.qq.com'
    #headers['User-Agent'] = 'curl/7.21.3 (i686-pc-linux-gnu) libcurl/7.21.3 OpenSSL/0.9.8o zlib/1.2.3.4 libidn/1.18'
    headers['User-Agent'] = ''

    data = dict()
    try:
        for i in request.form:
            data[i] = request.form[i]
        D = dianzan.Dianzan_verify()
        D.verify(data = data, headers = headers)
        ret = D.dianzan()
    except Exception as e:
        #logging.error(str(e) + str(data))
        print str(e) + str(data)
        ret = str(e)
        ret += "<hr/>"
        ret += "<p>%s</p>"%("用户名，密码或者验证码错误!请再试一次")
    return ret
