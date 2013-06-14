
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

        <!--div class="rain unfocus start">
            <div class="border unfocus start">
                <form id="login" action="/dianzan" method="post">
                    <label for="qq">qq</label>
                    <input name="qq" type="text" placeholder="qq">
                    <label for="pass">Password</label>
                    <input name="pwd" type="password" placeholder="Password">
                </form>
            </div>
            <input type="submit" value="confirm" onclick='document.getElementById("login").submit()'>
        </div-->
        <div id="container">
           <div class="description">
                 Recommended browsers: Safari, Chrome<br>
                       Alternate animation: Firefox 4<br>
                           </div>

                               <!-- Glowform -->
                                       <div class="rain unfocus start">
                                                <div class="border unfocus start">
                                                                <form>
                                                                                    <label for="email">Email</label>
                                                                                                        <input name="email" type="text" placeholder="Email">
                                                                                                                            <label for="pass">Password</label>
                                                                                                                                                <input name="pass" type="password" placeholder="Password">
                                                                                                                                                                </form>
                                                                                                                                                                            </div>
                                                                                                                                                                                        <input type="submit" value="LOG IN">
                                                                                                                                                                                                </div>
                                                                                                                                                                                                    <!-- /Glowform -->

                                                                                                                                                                                                        <h1><a href="http://github.com/kaylarose/Glowform">Glowform</a>
                                                                                                                                                                                                              <span class="small">by <a href="http://github.com/kaylarose">kaylarose</a></span></h1>

                                                                                                                                                                                                                  <div class="description">
                                                                                                                                                                                                                       CSS3 (image-less) Glowing Login Form (inspired by Dragon Labs).<br><br>
                                                                                                                                                                                                                             Webkit browsers recommended. Use Firefox 4 to see the fallback animation.
                                                                                                                                                                                                                                 </div>
                                                                                                                                                                                                                                     <p>
                                                                                                                                                                                                                                          * Disclaimer: This is meant as a CSS3 tech demo, not a best practices tutorial.
                                                                                                                                                                                                                                              </p>
                                                                                                                                                                                                                                                  <h2>Author(s)</h2>
                                                                                                                                                                                                                                                      <p>Kayla Martin (kayla.rose.martin@gmail.com &amp; http://gemdash.com)</p>


                                                                                                                                                                                                                                                          <h2>Download</h2>
                                                                                                                                                                                                                                                              <p>
                                                                                                                                                                                                                                                                    You can download this project in either
                                                                                                                                                                                                                                                                          <a href="http://github.com/kaylarose/Glowform/zipball/master">zip</a> or
                                                                                                                                                                                                                                                                                <a href="http://github.com/kaylarose/Glowform/tarball/master">tar</a> formats.
                                                                                                                                                                                                                                                                                    </p>
                                                                                                                                                                                                                                                                                        <p>You can also clone the project with <a href="http://git-scm.com">Git</a>
                                                                                                                                                                                                                                                                                              by running:
                                                                                                                                                                                                                                                                                                        </p><pre>$ git clone git://github.com/kaylarose/Glowform</pre>
                                                                                                                                                                                                                                                                                                            <p></p>

                                                                                                                                                                                                                                                                                                                <div class="footer">
                                                                                                                                                                                                                                                                                                                      get the source code on GitHub : <a href="http://github.com/kaylarose/Glowform">kaylarose/Glowform</a>
                                                                                                                                                                                                                                                                                                                          </div>

                                                                                                                                                                                                                                                                                                                            </div>
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
