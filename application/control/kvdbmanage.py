# -*- coding: utf-8 -*-

try:from application import app
except:pass

from flask import render_template
from flask import request
from flask import redirect, url_for

import json
import sys

from application.control.user import admin_required
from application.control import kvdbwrap

@app.route("/kvdbmanage")
@app.route("/kvdbmanage/<key>")
@admin_required
def kvdbmanage(key=None):
  if not key:
    return render_template("database.html")
  else:
    if key == "all": key=''
    with kvdbwrap.KVDB() as kv:
      key_values = kv.get_by_prefix(key)
    return render_template("kvdbmanage.html", values = key_values, name = key)

@app.route("/kvdbmanage/raw")
@app.route("/kvdbmanage/raw/<key>")
@admin_required
def kvdbmanage_row(key=None):
  if not key:
    return 'n/a'
  else:
    if key == "all": key=''
    with kvdbwrap.KVDB() as kv:
      key_values = kv.get_by_prefix(key)
      key_values = list(key_values)
    return json.dumps(key_values)

@app.route("/kvdb_add", methods = ["POST"])
@admin_required
def kvdb_add():
    with kvdbwrap.KVDB() as kv:
      key =  request.form['key']
      value = request.form['value']
      try:
          kv.add(key, value)
      except Exception as e:
          return "error"
          print e
    return 'kvdb_add'

@app.route("/kvdb_trash", methods = ["POST", "GET"])
@admin_required
def kvdb_trash():
    with kvdbwrap.KVDB() as kv:
      key =  request.form.get('key') or request.args.get('key', '')
      value = kv.get(key)
      try:
          ret = str( kv.delete(key) )
          kv.set("delete#" + key, value)
      except Exception as e:
          return "error:" + ret
          print e
    if request.referrer:
        return redirect(request.referrer)
    return redirect("/kvdbmanage/%s" % key.split('#')[0])

@app.route("/kvdb_del", methods = ["POST", "GET"])
@admin_required
def kvdb_del():
    #kv = sae.kvdb.KVClient()
    with kvdbwrap.KVDB() as kv:
      key = request.form.get('key') or request.args.get('key', '')
      ret = str( kv.delete(key) )
      key = "%s#" % key
    return redirect("/kvdbmanage/%s" % key.split('#')[0])

@app.route("/kvdb_set", methods = ["POST"])
@admin_required
def kvdb_set():
    with kvdbwrap.KVDB() as kv:
      key =  request.form.get('key') or request.args.get('key')
      value = request.form.get('value') or request.args.get('value')
      try:
          kv.set(key, value)
      except Exception as e:
          return "error"
          print e
    return 'kvdb_set'

@app.route("/kvdb_update", methods=['GET', 'POST'])
@admin_required
def kvdb_update():
  try:
    key = request.form.get('key') or request.args.get('key')
    item = request.form.get('value') or request.args.get('value')
    item = json.loads(item)
    #val = request.form.get('val') or request.args.get('val')
    with kvdbwrap.KVDB() as kv:
      items = kv.get(key)
      if items:
        items = json.loads(items)
        items.update(item)
        #if items.has_key(item.encode('utf-8')) or items.has_key(item.decode('utf-8')):
        #  items[item.encode('utf-8')] = val
        #  kv.set(key, json.dumps(items))
        kv.set(key, json.dumps(items))
        return 'success'
      return "no such items:" + key
  except Exception as e:
    return json.dumps({
      'ret': str(e)
      })
