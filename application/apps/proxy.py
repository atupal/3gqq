# -*- coding: utf-8 -*-

from application import app
from application.control.user import login_required
from flask import request
import requests
import json

@app.route('/proxy', methods=['GET', 'POST'])
@login_required
def proxy():
  type_ = request.args.get('type') or request.form.get('type', 'get')
  url = request.args.get('url') or request.form.get('url')
  data = request.args.get('data') or request.form.get('data', '{}')
  ret = 'error'
  if type_ == 'get':
    try:
      ret = requests.get(url, params = json.loads(data)).content
    except:
      import traceback, sys
      traceback.print_exc(file=sys.stdout)
      ret = 'error'
  elif type_ == 'post':
    try:
      ret = requests.post(url, data = json.loads(data)).content
    except:
      import traceback, sys
      traceback.print_exc(file=sys.stdout)
      ret = 'error'

  return ret
