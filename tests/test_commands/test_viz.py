import argparse
import io
import json

import pytest

from routes import commands
from routes import const


def make_result(path, metadata=None):
    if metadata is None:
        metadata = {}

    return {"path": path, "extra": {"metadata": metadata}}


def make_edge_node(name):
    return {"name": name, "fill": "white"}


@pytest.mark.parametrize(
    "data,expected",
    [
        (
            {
                "results": [
                    make_result("a/b.py"),
                    make_result("a/c.py"),
                    make_result("a/d.py"),
                ],
            },
            {
                "name": "a",
                "children": [
                    make_edge_node("b.py"),
                    make_edge_node("c.py"),
                    make_edge_node("d.py"),
                ],
            },
        ),
        (
            {
                "results": [
                    make_result("a/b/c/d/e.py"),
                    make_result("a/b/f.py"),
                    make_result("a/b/c/g/h.py"),
                ]
            },
            {
                "name": "a",
                "children": [
                    {
                        "name": "b",
                        "children": [
                            {
                                "name": "c",
                                "children": [
                                    {
                                        "name": "d",
                                        "children": [
                                            make_edge_node("e.py"),
                                        ],
                                    },
                                    {
                                        "name": "g",
                                        "children": [
                                            make_edge_node("h.py"),
                                        ],
                                    },
                                ],
                            },
                            make_edge_node("f.py"),
                        ],
                    },
                ],
            },
        ),
    ],
)
def test_viz_basic(data, expected):
    input = io.StringIO(json.dumps(data))
    output = io.StringIO()
    template = io.StringIO(const.DEFAULT_TEMPLATE_KEY)
    args = argparse.Namespace(input=input, output=output, template=template)

    code = commands.viz.main(args)
    result = json.loads(output.getvalue())

    input.close()
    output.close()
    template.close()

    assert code == 0
    assert result == expected


def test_viz_multiple_root():
    data = {
        "results": [
            make_result("a/b.py"),
            make_result("c/d.py"),
        ]
    }

    input = io.StringIO(json.dumps(data))
    output = io.StringIO()
    template = io.StringIO(const.DEFAULT_TEMPLATE_KEY)
    args = argparse.Namespace(input=input, output=output, template=template)

    with pytest.raises(ValueError):
        commands.viz.main(args)
