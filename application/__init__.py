
from flask import Flask

app = Flask(__name__)
app.DEBUG = True

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

@app.before_request
def before_request():
    pass

from application.apps.db_methods import init_db
db = init_db()

@app.teardown_request
def teardown_request(exception):
    try:db.close()
    except:pass
    print exception

from application.views import index
import application.views
