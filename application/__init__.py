
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

@app.teardown_request
def teardown_request(exception):
    print exception

from application.views import index
import application.views
