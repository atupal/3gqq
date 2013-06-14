
from application import app
from flask import request
#from application.apps import dianzan
import xml

@app.route('/')
def index():
    return '''
    <html>
        <form action="/dianzan" method="post">
            <input type="text" value="qq" name="qq"/>
            <input type="password" name="pwd" />
            <input type="submit" value="confirem">
        </form>
    </html>
    '''

@app.route('/dianzan', methods = ['POST'])
def dianzan():
    if request.method != 'POST':
        return 'methods not allowed!'
    qq = request.form.get('qq')
    pwd = request.form.get('pwd')
    D = dianzan.Dianzan(qq = qq, pwd = pwd)
    D.dianzan()

