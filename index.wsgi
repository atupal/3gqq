import sae

def app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/html; charset=utf-8')]
    start_response(status, response_headers)
    return ['<strong>Welcome to SAE!</strong>']

application = sae.create_wsgi_app(app)