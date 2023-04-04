import pathlib


CURDIR = pathlib.Path(__file__).parent
TEST_ROUTE_DETECT = CURDIR / "test-route-detect.yml"
FLASK = CURDIR / "flask.yml"
DJANGO = CURDIR / "django.yml"
DJANGO_REST_FRAMEWORK = CURDIR / "django-rest-framework.yml"
SANIC = CURDIR / "sanic.yml"
LARAVEL = CURDIR / "laravel.yml"
SYMFONY = CURDIR / "symfony.yml"
CAKEPHP = CURDIR / "cakephp.yml"
RAILS = CURDIR / "rails.yml"
GRAPE = CURDIR / "grape.yml"
JAXRS = CURDIR / "jax-rs.yml"
SPRING = CURDIR / "spring.yml"
GORILLA = CURDIR / "gorilla.yml"
GIN = CURDIR / "gin.yml"
CHI = CURDIR / "chi.yml"
EXPRESS = CURDIR / "express.yml"
REACT = CURDIR / "react.yml"
ANGULAR = CURDIR / "angular.yml"

# Specifying the rules directory will run all rule files within
ALL = CURDIR

ALL_RULES = {
    **{
        str(rule.with_suffix("").name): str(rule.resolve())
        for rule in [
            TEST_ROUTE_DETECT,
            FLASK,
            DJANGO,
            DJANGO_REST_FRAMEWORK,
            SANIC,
            LARAVEL,
            SYMFONY,
            CAKEPHP,
            RAILS,
            GRAPE,
            JAXRS,
            SPRING,
            GORILLA,
            GIN,
            CHI,
            EXPRESS,
            REACT,
            ANGULAR,
        ]
    },
    **{"all": ALL},
}
