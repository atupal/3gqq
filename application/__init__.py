# -*- coding: utf-8 -*-

from flask import Flask

app = Flask(__name__, static_url_path = "")

#import ConfigParser
#import os
#import logging

#config = ConfigParser.RawConfigParser()

#with open('./env.cfg','w') as fi:
#    config.add_section('dir')
#    config.set('dir', 'root', os.path.abspath('.'))
#    config.write(fi)
#

#logging.basicConfig(filename= 'logs/debug.log',level=logging.DEBUG)
#logging.debug('tess')

from component.redis_session import RedisSessionInterface
app.session_interface = RedisSessionInterface()

import os
app.config.update(
    #使用session必须要配置secret key
    SECRET_KEY=os.urandom(32).encode('hex')
    )

app.config.from_object('application.config')

import urllib
@app.template_filter('urlquote')
def urlquote(uri):
  return urllib.quote(uri)
app.jinja_env.globals['urlquote'] = urlquote

@app.before_request
def before_request():
    pass

from application.apps.db_methods import init_db
db = init_db()

@app.teardown_request
def teardown_request(exception):
    try:db.close()
    except:pass

# views
from application.views import index
# control
from application.control import qq
from application.control import user
from application.control import kvdbmanage
# apps
from application.apps import proxy
