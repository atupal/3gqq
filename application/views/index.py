
from application import app

@app.route('/')
def index():
    return '''
    <html>
        <form action="/dianzan">
            <input type="text" value="qq" name="qq"/>
            <input type="text" value="pwd" name="pwd" />
            <input type="submit" value="confirem">
        </form>
    </html>
    '''

