import pytest

from routes import util


@pytest.mark.parametrize(
    "s,expected",
    [
        ("snake_case", "SnakeCase"),
        ("snake", "Snake"),
        ("", ""),
    ],
)
def test_pascal_case(s, expected):
    result = util.pascal_case(s)

    assert result == expected
