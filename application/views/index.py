
from application import app

@app.route('/')
def index():
    return '''
    <html>
        <form action="/dianzan">
            <input type="text" value="qq" />
            <input type="text" value="pwd" />
            <input type="submit" value="confirem">
        </form>
    </html>
    '''

