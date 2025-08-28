import enum

from routes import const


class ResultType(enum.Enum):
    ROUTE = "route"
    GLOBAL = "global"


class Framework(enum.Enum):
    FLASK = "flask"
    DJANGO = "django"
    DJANGO_REST_FRAMEWORK = "django-rest-framework"
    SANIC = "sanic"
    LARAVEL = "laravel"
    SYMFONY = "symfony"
    CAKEPHP = "cakephp"
    RAILS = "rails"
    GRAPE = "grape"


class SemgrepResult:
    def __init__(self, result):
        self.result = result

    @property
    def check_id(self):
        return self.result["check_id"]

    @property
    def path(self):
        return self.result["path"]

    @property
    def start_line(self):
        return self.result["start"]["line"]

    @property
    def lines(self):
        return self.result["extra"]["lines"]

    @property
    def first_line(self):
        newline = self.lines.find("\n")
        return self.lines[:newline] if newline != -1 else self.lines

    @property
    def metadata(self):
        return self.result["extra"].get("metadata", {})

    @property
    def metavars(self):
        return self.result["extra"]["metavars"]

    def metavar_content(self, metavar):
        return self.metavars[metavar]["abstract_content"]

    @property
    def rd_metadata(self):
        return self.metadata.get("route-detect", {})

    @property
    def rd_type(self):
        return self.rd_metadata.get("type", ResultType.ROUTE.value)

    @property
    def rd_fill(self):
        return self.rd_metadata.get("fill", const.DEFAULT_FILL_COLOR)
