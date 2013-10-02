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
import json

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')
    with kvdbwrap.KVDB() as kv:
      ret = json.loads(kv.get('user#admin'))
      if email.split('@')[0] == 'admin' and password == ret.get('password'):
        session['user'] = 'admin'
    if request.args.get('next'):
      return redirect(request.args.get('next'))
  return render_template('login.html')

@app.route('/logout')
def logout():
  session.pop('user', None)
  return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  return render_template('signup.html')


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
