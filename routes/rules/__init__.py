import pathlib


CURDIR = pathlib.Path(__file__).parent
TEST_ROUTE_DETECT = CURDIR / "test-route-detect.yml"
FLASK = CURDIR / "flask.yml"
DJANGO = CURDIR / "django.yml"
DJANGO_REST_FRAMEWORK = CURDIR / "django-rest-framework.yml"
SANIC = CURDIR / "sanic.yml"

ALL_RULES = {
    str(rule.with_suffix("").name): str(rule.resolve())
    for rule in [
        TEST_ROUTE_DETECT,
        FLASK,
        DJANGO,
        DJANGO_REST_FRAMEWORK,
        SANIC,
    ]
}
