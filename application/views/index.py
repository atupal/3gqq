#-*- coding=utf-8 -*-

from application import app
from flask import request
from flask import render_template

from application.apps import dianzan
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from application.apps.db_methods import add_task
from application.apps.db_methods import init_db
import logging
import traceback

#from application import db


@app.route('/')
def index():
    db = init_db()
    cursor = db.cursor()
    cursor.execute('''select * from feedback''')
    ret = cursor.fetchall()
    try:ret_list = [ [ _[1] , _[2], _[3] ] for _ in ret ]
    except:ret_list = [ ['error', 'error', 'error'] ]

    return render_template('index.html', comments = ret_list)

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
        except Exception as e: print e; traceback.print_exc(file = sys.stdout)


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

        if str(frr) == "on":
            try:ret = D.get_friend()
            except:ret={}
            if len(ret) == 0:
                return '''
                        <html>
                        <body>
                            </p>妈蛋, 好像获取好友列表失败了,<a href="/">再试一次</a>吧</p>
                        </body>
                        </html>

                        '''
            return render_template('select_friend.html', frr = ret)

    except Exception as e:
        #logging.error(str(e))
        print str(e)
        traceback.print_exc(file=sys.stdout)
        ret = "<p>%s</p>"%("用户名，密码或者验证码错误!请再试一次")
        ret += '<script> console.log("%s") </script>' % str(e)
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
        traceback.print_exc(file=sys.stdout)
        ret = "<p>%s</p>"%("用户名，密码或者验证码错误!请再试一次")
        ret += '<script> console.log("%s") </script>' % str(e)
    return ret


@app.route('/feedback', methods = ['POST'])
def feedback():
    db = init_db()
    nickname = request.form.get('nickname', '这个人很懒什么都没留下')
    contact = request.form.get('contact', '这个人很懒什么都没留下')
    comment = request.form.get('comment', '妈蛋, 这个人什么都没写')

    import MySQLdb
    nickname = MySQLdb.escape_string(nickname)
    contact = MySQLdb.escape_string(contact)
    comment = MySQLdb.escape_string(comment)
    sql = r'''
                insert feedback (nickname, contact, comment) values ("%s", "%s", "%s");
        ''' % (nickname, contact, comment)
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    db.close()
    return r'''
        <html>
            <p> 评论成功, <a href="/">点击</a>返回  </p>
        </html>
    '''
