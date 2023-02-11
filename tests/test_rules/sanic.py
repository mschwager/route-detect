from sanic import Sanic

app = Sanic("MyHelloWorldApp")


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
