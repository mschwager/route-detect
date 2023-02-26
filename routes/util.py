import itertools
import json


def pascal_case(s):
    # E.g. "snake_case" -> "SnakeCase"
    return s.replace("_", " ").title().replace(" ", "")


def sorted_groupby(iterable, key):
    return itertools.groupby(sorted(iterable, key=key), key=key)


def compact_dumps(data):
    return json.dumps(data, separators=(",", ":"))
