from flask import Flask
from flask.views import MethodView
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'


class HttpMethodExample(MethodView):
    def get(self):
        return 'Send request with `GET` method'

    def post(self):
        return 'Send request with `POST` method'

    def put(self):
        return 'Send request with `PUT` method'

    def patch(self):
        return 'Send request with `PATCH` method'

    def delete(self):
        return 'Send request with `DELETE` method'

app.add_url_rule('/http-method-test2/', view_func=HttpMethodExample.as_view('http_method_example2'))

if __name__ == '__main__':
    app.run()