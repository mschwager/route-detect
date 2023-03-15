import flask_praetorian

from flask import Flask
from flask.views import View
from flask_login import login_required, fresh_login_required
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import jwt_required

app = Flask(__name__)
auth = HTTPBasicAuth()


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
@flask_praetorian.auth_required
def hello_world():
    return "<p>Hello, World!</p>"


# ruleid: flask-route-authenticated
@app.route("/")
@login_required
def hello_world():
    return "<p>Hello, World!</p>"


# ruleid: flask-route-authenticated
@app.route("/")
@fresh_login_required
def hello_world():
    return "<p>Hello, World!</p>"


# ruleid: flask-route-authenticated
@app.route("/")
@requires_authentication
def hello_world():
    return "<p>Hello, World!</p>"


# ruleid: flask-route-authenticated
@app.route("/")
@auth.login_required
def hello_world():
    return "<p>Hello, World!</p>"


# ruleid: flask-route-authenticated
@app.route("/")
@jwt_required
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


# ruleid: flask-route-unauthenticated
class UserList(View):
    def dispatch_request(self):
        users = User.query.all()
        return render_template("users.html", objects=users)


# ruleid: flask-route-authenticated
class UserList(View):
    decorators = [login_required]
    def dispatch_request(self):
        users = User.query.all()
        return render_template("users.html", objects=users)


# todoruleid: flask-route-authenticated, flask-route-unauthenticated
class UserList(View):
    decorators = [login_required("argument")]
    def dispatch_request(self):
        users = User.query.all()
        return render_template("users.html", objects=users)


app.add_url_rule("/users/", view_func=UserList.as_view("user_list"))
