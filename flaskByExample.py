from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    query = request.args.get('publication')
    print query
    return 'Hello World!'


if __name__ == '__main__':
    app.run(port=5000, debug=True)
