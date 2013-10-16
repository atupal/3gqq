# -*- coding: utf-8 -*-

from functools import wraps

from flask import g
from flask import redirect
from flask import url_for
from flask import request
from flask import render_template
from flask import session

from application import app
from application.control import kvdbwrap
from application.component import mail
import json
import hashlib
import os
import urllib
import time

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')
    with kvdbwrap.KVDB() as kv:
      ret = json.loads(kv.get('user#admin'))
      if email.split('@')[0] == 'admin' and password == ret.get('password'):
        session.permanent = True  # make the session permanent after closing the  brower
        session['user'] = 'admin'

    try:
      with kvdbwrap.KVDB() as kv:
        ret = json.loads(kv.get('user#%s' % email))
        if password == ret.get('password'):
            session['user'] = ret.get('nick')
    except:
      pass

    if request.args.get('next'):
      return redirect(request.args.get('next'))
  return render_template('login.html')

@app.route('/logout')
def logout():
  session.pop('user', None)
  return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'POST':
    data = {}
    data['email'] = request.form.get('email', '').strip()
    with kvdbwrap.KVDB() as kv:
      if kv.get("user#%s" % data['email']):
        ret = {'code': '-1', 'msg': '此邮箱已经被注册'}
        return json.dumps(ret)
    with kvdbwrap.KVDB() as kv:
      if kv.get("verify#%s" % data['email']):
        ret = {'code': '-1', 'msg': '此邮箱正在激活中！'}
        return json.dumps(ret)

    data['nick'] = request.form.get('nick', '').strip()
    data['qq'] = request.form.get('qq', '').strip()
    data['password'] = request.form.get('password', '')
    cid = hashlib.md5(os.urandom(32)).hexdigest()
    url = 'http://3gqq67.sinaapp.com/email_verify?cid=%s&email=%s' % (urllib.quote(cid), urllib.quote(data['email']))
    with kvdbwrap.KVDB() as kv:
      data['cid'] = cid
      data['init_time'] = int(time.time())
      kv.add('verify#%s' % data['email'], json.dumps(data))
    content = '''
      请在浏览器中打开此链接完成注册:
      <a href="%s">%s</a>
    ''' % (url, url)
    mail.send_email(content = content, to_email = data.get('email'))
    ret = {'code': '0', 'msg': '注册成功！请前往你的邮件箱激活账号'};
    return json.dumps(ret)
  return render_template('signup.html')

@app.route('/email_verify')
def email_verify():
  cid = request.args.get('cid')
  email = request.args.get('email')
  ret = {}
  with kvdbwrap.KVDB() as kv:
    try:
      ret = json.loads(kv.get('verify#%s' % email))
    except:
      pass
  if ret.get('cid') == cid:
    ret.pop('cid')
    ret.pop('init_time')
    with kvdbwrap.KVDB() as kv:
      kv.add('user#%s' % email, json.dumps(ret))
    with kvdbwrap.KVDB() as kv:
      kv.delete('verify#%s' % email)
    return redirect(url_for('login'))
  else:
    return '激活失败！'

def admin_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if session.get('user') != 'admin':
      return redirect(url_for('login', next=request.url))
    return f(*args, **kwargs)
  return decorated_function

def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if session.get('user', None) is None:
      return redirect(url_for('login', next=request.url))
    return f(*args, **kwargs)
  return decorated_function
