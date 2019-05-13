from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
    return 'hello'


@app.route('/login')
def login():
    return 'login'


@app.route('/logout')
def logout():
    return 'logout'


@app.errorhandler(404)
def page_not_found(e):
    return '404'
    # return e


if __name__ == '__main__':
    app.run()