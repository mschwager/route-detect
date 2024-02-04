import enum

from routes import const


class ResultType(enum.Enum):
    ROUTE = "route"
    CONNECTOR = "connector"
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
    SPRING = "spring"


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

    # Try to extract a route from the result, it's not in the metadata and has to be parsed from the line
    @property
    def rd_route(self):
        if "$PATH" in self.metavars: #For some rules we have extracted a path in the $PATH metavar
            return "{} {}".format(self.rd_method, self.metavars['$PATH']['abstract_content'])
        elif self.rd_type == ResultType.ROUTE.value:
            return self.first_line
        else:
            return None
    
    @property
    def rd_method(self):
        # split by space and deduplicate and return first element
        return list(set(self.metavars['$METHOD']['abstract_content'].split(' ')))[0]

    @property
    def rd_normalizer(self):
        return self.rd_metadata.get("normalizer")

    @property
    def rd_fill(self):
        return self.rd_metadata.get("fill", const.DEFAULT_FILL_COLOR)

    @property
    def rd_connect_on(self):
        return self.rd_metadata["connect-on"]
