import sanic_beskar

from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic_jwt.decorators import protected
from sanic_jwt_extended import jwt_required
from sanic_security.authentication import requires_authentication
from sanic_ext import openapi
from sanic_token_auth import SanicTokenAuth
from sanic_httpauth import HTTPDigestAuth
from sanic_auth import Auth
from SanicApiKey import SanicApiKey

app = Sanic("MyHelloWorldApp")
token_auth = SanicTokenAuth(app, secret_key="test", header="X-My-App-Auth-Token")
digest_auth = HTTPDigestAuth()
auth = Auth(app)
api_auth = SanicApiKey(app, 'api_key', keys=['hello', 'world'], error=test)


# ruleid: sanic-route-unauthenticated
@app.route("/test", methods=["POST", "PUT"])
async def handler(request):
    return text("OK")


# ruleid: sanic-route-unauthenticated
app.add_route(handler, "/test")


# ruleid: sanic-route-unauthenticated
@app.get("/test")
async def handler(request):
    return text("OK")


# ruleid: sanic-route-authenticated
@app.route("/protected")
@protected()
async def protected_route(request):
    return json({"protected": True})


# ruleid: sanic-route-authenticated
@app.route("/jwt_required")
@jwt_required()
async def jwt_required_route(request):
    return json({"protected": True})


# ruleid: sanic-route-authenticated
@app.post("api/security/auth")
@requires_authentication()
async def on_authenticate(request, authentication_session):
    return json(
        "You have been authenticated.",
        authentication_session.bearer.json(),
    )


# ruleid: sanic-route-authenticated
@app.route("/two")
@openapi.secured("foo")
async def handler2(request):
    return text("OK")


# ruleid: sanic-route-authenticated
@app.route("/three")
@openapi.definition(secured="foo")
async def handler3(request):
    return text("OK")


# ruleid: sanic-route-authenticated
@app.route("/protected")
@token_auth.auth_required
async def protected(request):
    return text("Welcome!")


# ruleid: sanic-route-authenticated
@app.route("/")
@digest_auth.login_required
def index(request):
    return response.text(f"Hello, {auth.username(request)}!")


# ruleid: sanic-route-authenticated
@app.route('/profile')
@auth.login_required(user_keyword='user')
async def profile(request, user):
    return response.json({'user': user})


# ruleid: sanic-route-authenticated
@app.route("/protected")
@sanic_beskar.auth_required
async def protected(request):
    user = await sanic_beskar.current_user()
    return json({"message": f"protected endpoint (allowed user {user.username})"})


# ruleid: sanic-route-authenticated
@app.route('/')
@auth.key_required
async def test(request):
    return json({'success': True, 'key': auth.get_token()})


# todoruleid: sanic-route-authenticated
class ViewWithDecorator(HTTPMethodView):
    decorators = [login_required]

    def get(self, request, name):
        return text("Hello I have a decorator")


# todoruleid: sanic-route-unauthenticated
class ViewWithDecorator(HTTPMethodView):
    decorators = []

    def get(self, request, name):
        return text("Hello I have a decorator")
