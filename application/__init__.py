
from flask import Flask

app = Flask(__name__)

@app.before_request
def before_request():
    pass

@app.teardown_request
def teardown_request(exception):
    print exception

from application.views import index
