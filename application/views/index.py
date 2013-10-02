#-*- coding: utf-8 -*-

from application import app
from flask import request
from flask import render_template

from application.apps import dianzan
import sys

from application.apps.db_methods import add_task
from application.apps.db_methods import init_db
import logging
import traceback
from pprint import pprint as printf

#from application import db
from application.control import kvdbwrap
from flask import session
import json

@app.route('/')
def index():
  return render_template('layout.html')

@app.route('/origin')
def index_origin():
    db = init_db()
    cursor = db.cursor()
    cursor.execute('''select * from feedback order by id DESC''')
    ret = cursor.fetchall()
    try:ret_list = [ [ _[1].encode('utf-8') , _[2].encode('utf-8'), _[3].encode('utf-8') ] for _ in ret ]
    except:ret_list = [ ['error', 'error', 'error'] ]

    return render_template('index.html', comments = ret_list)

@app.route('/dianzan_qq')
def dianzan_qq():
  data = {}
  if 'qq' in session:
    with kvdbwrap.KVDB() as kv:
      try:
        data = json.loads(kv.get('qq#%s' % session['qq']))
      except:pass
  return render_template('dianzan_qq.html', data = data)
