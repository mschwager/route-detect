import pathlib

import pytest

from routes import queries


@pytest.mark.parametrize("query", queries.ALL_QUERIES.values())
def test_query_paths_exists(query):
    assert pathlib.Path(query).exists()
