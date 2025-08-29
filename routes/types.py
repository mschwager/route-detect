import abc
import enum
import json

from routes import const


class ResultType(enum.Enum):
    ROUTE = "route"
    GLOBAL = "global"


class BaseOutput:
    def __init__(self, output):
        self.output = output

    @classmethod
    def from_fd(cls, fd):
        return cls(json.load(fd))

    @property
    @abc.abstractmethod
    def results(self):
        pass


class BaseResult(abc.ABC):
    @property
    @abc.abstractmethod
    def id(self):
        pass

    @property
    @abc.abstractmethod
    def path(self):
        pass

    @property
    @abc.abstractmethod
    def start_line(self):
        pass

    @property
    @abc.abstractmethod
    def lines(self):
        pass

    @property
    @abc.abstractmethod
    def first_line(self):
        pass

    @property
    def rd_type(self):
        return ResultType.ROUTE.value

    @property
    def rd_fill(self):
        return const.DEFAULT_FILL_COLOR


class SemgrepResult(BaseResult):
    def __init__(self, result):
        self.result = result

    @property
    def id(self):
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


class SemgrepOutput(BaseOutput):
    @property
    def results(self):
        return [SemgrepResult(r) for r in self.output["results"]]


class CodeQLResult(BaseResult):
    def __init__(self, result, output):
        self.result = result
        self.output = output

        # Assume last location provides the relevant code snippet
        self.location = self.result["locations"][-1]["physicalLocation"]

    @property
    def id(self):
        return self.result["rule"]["id"]

    @property
    def path(self):
        # TODO find more robust way to ensure all result paths have a single root directory
        return "repo" + "/" + self.location["artifactLocation"]["uri"]

    @property
    def artifact_index(self):
        return self.location["artifactLocation"]["index"]

    @property
    def start_line(self):
        return self.location["region"]["startLine"]

    @property
    def end_line(self):
        return self.location["region"].get("endLine", self.start_line)

    @property
    def lines(self):
        artifact = self.output.first_run["artifacts"][self.artifact_index]

        # --sarif-add-file-contents provides this data
        contents = artifact.get("contents", {}).get("text", "")
        if not contents:
            return []

        context = 1

        # -1 for 0-based indexing
        start = max(self.start_line - context - 1, 0)
        end = self.end_line + context
        lines = contents.split("\n")

        return "\n".join(lines[start:end])

    @property
    def first_line(self):
        # We provide 1 line of context above and below the result's line, so
        # the result's line should be the middle list index of 3 elements
        return self.lines.split("\n")[1]


class CodeQLOutput(BaseOutput):
    @property
    def first_run(self):
        # Assume we only have a single run
        return self.output["runs"][0]

    @property
    def results(self):
        return [CodeQLResult(r, self) for r in self.first_run["results"]]
