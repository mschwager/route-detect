from flask import Flask

app = Flask(__name__)

# ruleid: flask-route-unauthenticated
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# ruleid: flask-route-authenticated
@app.route("/")
@auth_required
def hello_world():
    return "<p>Hello, World!</p>"


# ruleid: flask-route-authenticated
@app.route("/")
@login_required
def hello_world():
    return "<p>Hello, World!</p>"


# ruleid: flask-route-authenticated
@app.route("/")
@requires_authentication
def hello_world():
    return "<p>Hello, World!</p>"


# ruleid: flask-route-authenticated
@app.route("/")
@foobar
@auth_required
def hello_world():
    return "<p>Hello, World!</p>"


# ruleid: flask-route-authenticated
@app.route("/")
@foobar
@login_required
def hello_world():
    return "<p>Hello, World!</p>"


# ruleid: flask-route-authenticated
@app.route("/")
@foobar
@requires_authentication
def hello_world():
    return "<p>Hello, World!</p>"
