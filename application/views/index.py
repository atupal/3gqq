
from application import app
from flask import request
from application.apps import dianzan

@app.route('/')
def index():
    return '''
    <html>
        <style>
            form{
            margin: 0px;
            padding: 4px;
            }

            label{
            width: 80px;
            float: left;
            text-align: right;
            padding: 3px 0px 1px;
            color: #666666;
            }

            input{
            border: 1px solid #CCCCCC;
            margin: 1px;
            padding: 1px;
            font-family: Arial;
            font-size: 12px;
            color: #666666;
            }

            .bt{
            width: 44px;
            height: 20px;
            font-size: 10px;
            color: #333333;
            border: solid 1px #CCCCCC;
            background: #FBFBFB;
            }
        </style>
        <body>
            <form id="login" action="/dianzan" method="post">
                <label for="qq">qq</label>
                <input name="qq" type="text" placeholder="qq">
                <label for="pass">Password</label>
                <input name="pwd" type="password" placeholder="Password">
                <input type="submit" value="confirm" class="bt">
            </form>
        </body>
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
