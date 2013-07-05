
import os, sys
sys.path.append(os.path.realpath(__file__))



from application import app

#def app(environ, start_response):
#    status = '200 OK'
#    response_headers = [('Content-type', 'text/html; charset=utf-8')]
#    start_response(status, response_headers)
#    return ['<strong>Welcome to SAE!</strong>']

if "HOME" in os.environ.keys() and os.environ['HOME'] == "/home/atupal":
    app.run('0.0.0.0', 8080)
else:
    import sae
    application = sae.create_wsgi_app(app)


