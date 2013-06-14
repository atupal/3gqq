
from application import app
from flask import request
from application.apps import dianzan

@app.route('/')
def index():
    return '''
    <html>
        <style type="text/css">embed[type*="application/x-shockwave-flash"],embed[src*=".swf"],object[type*="application/x-shockwave-flash"],object[codetype*="application/x-shockwave-flash"],object[src*=".swf"],object[codebase*="swflash.cab"],object[classid*="D27CDB6E-AE6D-11cf-96B8-444553540000"],object[classid*="d27cdb6e-ae6d-11cf-96b8-444553540000"],object[classid*="D27CDB6E-AE6D-11cf-96B8-444553540000"]{   display: none !important;}</style>
        <!--form action="/dianzan" method="post">
            <input type="text" value="qq" name="qq"/>
            <input type="password" name="pwd" />
            <input type="submit" value="confirem">
        </form-->
        <form id="login" action="/dianzan" method="post">
            <label for="qq">qq</label>
            <input name="qq" type="text" placeholder="qq">
            <br/>
            <label for="pass">Password</label>
            <input name="pwd" type="password" placeholder="Password">
            <br/>
            <input type="submit" value="confirm">
        </form>
    </html>
    '''

@app.route('/dianzan', methods = ['POST'])
def _dianzan():
    if request.method != 'POST':
        return 'methods not allowed!'
    qq = request.form.get('qq')
    pwd = request.form.get('pwd')
    D = dianzan.Dianzan(qq = qq, pwd = pwd)
    return D.dianzan()

@app.route('/dianzan_verify', methods = ['POST'])
def _dianzan_verify():
    if request.method != 'POST':
        return 'methods not allowed!'
    headers = dict()
    headers['Origin'] = 'http://pt.3g.qq.com'
    headers['Host'] = 'pt.3g.qq.com'
    #headers['User-Agent'] = 'curl/7.21.3 (i686-pc-linux-gnu) libcurl/7.21.3 OpenSSL/0.9.8o zlib/1.2.3.4 libidn/1.18'
    headers['User-Agent'] = ''

    D = dianzan.Dianzan_verify()
    data = dict()
    for i in request.form:
        data[i] = request.form[i]
    D.verify(data = data, headers = headers)
    return D.dianzan()
