import pathlib

from routes import rules


def test_rule_paths_exists():
    assert all(pathlib.Path(p).exists() for p in rules.ALL_RULES.values())
