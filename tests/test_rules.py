import pathlib

import pytest

from routes import rules


@pytest.mark.parametrize("rule", rules.ALL_RULES.values())
def test_rule_paths_exists(rule):
    assert pathlib.Path(rule).exists()
