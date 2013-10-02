
import os, sys
sys.path.insert(0, os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

from application import app
app.debug = True

#def app(environ, start_response):
#    status = '200 OK'
#    response_headers = [('Content-type', 'text/html; charset=utf-8')]
#    start_response(status, response_headers)
#    return ['<strong>Welcome to SAE!</strong>']

if __name__ == "__main__" and "HOME" in os.environ.keys() and os.environ['HOME'] == "/home/atupal":
    app.run('0.0.0.0', 8080)
else:
    import sae
    application = sae.create_wsgi_app(app)
