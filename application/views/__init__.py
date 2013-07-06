
from application import app

@app.route('/static/<path:name>', methods = ['GET'])
@app.route('/static/<name>', methods = ['GET'])
def staticfile(name):
    print name
    fi = open("application/static/" + name)
    return fi.read()
