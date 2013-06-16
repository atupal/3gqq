#-*- coding=utf-8 -*-

from application import app
from flask import request
from application.apps import dianzan
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

@app.route('/')
def index():
    return '''
    <html>
        <style>
            .github-fork-ribbon{position:absolute;padding:2px 0;background-color:#a00;background-image:-webkit-gradient(linear,left top,left
            bottom,from(rgba(0,0,0,0.00)),to(rgba(0,0,0,0.15)));background-image:-webkit-linear-gradient(top,rgba(0,0,0,0.00),rgba(0,0,0,0.15));background-image:-moz-linear-gradient(top,rgba(0,0,0,0.00),rgba(0,0,0,0.15));background-image:-o-linear-gradient(top,rgba(0,0,0,0.00),rgba(0,0,0,0.15));background-image:-ms-linear-gradient(top,rgba(0,0,0,0.00),rgba(0,0,0,0.15));background-image:linear-gradient(top,rgba(0,0,0,0.00),rgba(0,0,0,0.15));filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,StartColorStr='#000000',EndColorStr='#000000');-webkit-box-shadow:0
            2px 3px 0 rgba(0,0,0,0.5);box-shadow:0 2px 3px 0 rgba(0,0,0,0.5);z-index:9999}.github-fork-ribbon a,.github-fork-ribbon a:hover{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:13px;font-weight:700;color:white;text-decoration:none;text-shadow:0 -1px rgba(0,0,0,0.5);text-align:center;width:200px;line-height:20px;display:inline-block;padding:2px 0;border-width:1px
            0;border-style:dotted;border-color:rgba(255,255,255,0.7)}.github-fork-ribbon-wrapper{width:150px;height:150px;position:absolute;overflow:hidden;top:0;z-index:9999}.github-fork-ribbon-wrapper.fixed{position:fixed}.github-fork-ribbon-wrapper.left{left:0}.github-fork-ribbon-wrapper.right{right:0}.github-fork-ribbon-wrapper.left-bottom{position:fixed;top:inherit;bottom:0;left:0}.github-fork-ribbon-wrapper.right-bottom{position:fixed;top:inherit;bottom:0;right:0}.github-fork-ribbon-wrapper.right
            .github-fork-ribbon{top:42px;right:-43px;-webkit-transform:rotate(45deg);-moz-transform:rotate(45deg);-o-transform:rotate(45deg);transform:rotate(45deg)}.github-fork-ribbon-wrapper.left .github-fork-ribbon{top:42px;left:-43px;-webkit-transform:rotate(-45deg);-moz-transform:rotate(-45deg);-o-transform:rotate(-45deg);transform:rotate(-45deg)}.github-fork-ribbon-wrapper.left-bottom
            .github-fork-ribbon{top:80px;left:-43px;-webkit-transform:rotate(45deg);-moz-transform:rotate(45deg);-o-transform:rotate(45deg);transform:rotate(45deg)}.github-fork-ribbon-wrapper.right-bottom .github-fork-ribbon{top:80px;right:-43px;-webkit-transform:rotate(-45deg);-moz-transform:rotate(-45deg);-o-transform:rotate(-45deg);transform:rotate(-45deg)}
        </style>
        <body>
            <form id="login" action="/dianzan" method="post">
                <input name="qq" type="text" placeholder="qq">
                <br/>
                <input name="pwd" type="password" placeholder="Password">
                <br/>

                <label>点赞页数</label>
                <select name="cnt">
                <option value="volvo">1</option>
                <option value="volvo">2</option>
                <option value="saab">3</option>
                <option value="fiat">4</option>
                <option value="audi">5</option>
                </select>
                <br>
                <label>点赞次数</label>
                <select name="feq">
                <option value="volvo">1</option>
                <option value="volvo">5</option>
                <option value="saab">10</option>
                <option value="fiat">20</option>
                <option value="audi">50</option>
                <option value="audi">100</option>
                </select>
                <br>
                <label>点赞间隔(min)</label>
                <select name="inc">
                <option value="volvo">5</option>
                <option value="volvo">10</option>
                <option value="saab">30</option>
                <option value="fiat">60</option>
                <option value="audi">120</option>
                </select>
                <br>
                <input type="submit" value="confirm" class="bt">
            </form>
            <p>web版的点赞次数和间隔还没实现,等考试完再弄吧</p>
            <strong>很多人问我有没有记录密码,,,没有,没有记录任何东西,你可以看下源代码(右上角)</strong>


            <div class="github-fork-ribbon-wrapper right">
                <div class="github-fork-ribbon">
                    <a href="https://github.com/atupal/3gqq/blob/master/dianzan/dianzan_py-dom-xpath.py">Fork me on GitHub</a>
                </div>
            </div>
        </body>
    </html>
    '''

@app.route('/dianzan', methods = ['POST'])
def _dianzan():
    if request.method != 'POST':
        return 'methods not allowed!'
    qq = request.form.get('qq')
    pwd = request.form.get('pwd')
    #cnt = request.form.get('cnt')
    #feq = request.form.get('feq')
    #inc = request.form.get('inc')
    try:
        D = dianzan.Dianzan(qq = qq, pwd = pwd)
        ret = D.dianzan(cnt = 5)
    except Exception as e:
        ret = e
        ret += "<hr/>"
        ret += "<p>%s</p>"%("用户名，密码错误，请再试一次")
    return ret

@app.route('/dianzan_verify', methods = ['POST'])
def _dianzan_verify():
    if request.method != 'POST':
        return 'methods not allowed!'
    headers = dict()
    headers['Origin'] = 'http://pt.3g.qq.com'
    headers['Host'] = 'pt.3g.qq.com'
    #headers['User-Agent'] = 'curl/7.21.3 (i686-pc-linux-gnu) libcurl/7.21.3 OpenSSL/0.9.8o zlib/1.2.3.4 libidn/1.18'
    headers['User-Agent'] = ''

    data = dict()
    for i in request.form:
        data[i] = request.form[i]
    try:
        D = dianzan.Dianzan_verify()
        D.verify(data = data, headers = headers)
        ret = D.dianzan()
    except Exception as e:
        ret = e
        ret += "<hr/>"
        ret += "<p>%s</p>"%("用户名，密码或者验证码错误!请再试一次")
    return ret
