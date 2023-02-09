import argparse
import io
import json

import pytest

from routes import commands
from routes import const


def make_result(lines, path, metadata=None):
    if metadata is None:
        metadata = {}

    return {
        "path": path,
        "extra": {"metadata": metadata, "lines": lines},
        "start": {"line": 0},
    }


def make_edge_node(name):
    return {"name": f"ln 0: {name}", "fill": "white"}


@pytest.mark.parametrize(
    "data,expected",
    [
        (
            {
                "results": [
                    make_result("c1", "a/b.py"),
                    make_result("c2", "a/c.py"),
                ],
            },
            {
                "name": "a",
                "children": [
                    {"name": "b.py", "children": [make_edge_node("c1")]},
                    {"name": "c.py", "children": [make_edge_node("c2")]},
                ],
            },
        ),
        (
            {
                "results": [
                    make_result("c1", "a/b.py"),
                    make_result("c1", "a/c.py"),
                ],
            },
            {
                "name": "a",
                "children": [
                    {"name": "b.py", "children": [make_edge_node("c1")]},
                    {"name": "c.py", "children": [make_edge_node("c1")]},
                ],
            },
        ),
        (
            {
                "results": [
                    make_result("c1", "a/b.py"),
                    make_result("c1", "a/b.py"),
                ],
            },
            {
                "name": "a",
                "children": [
                    {
                        "name": "b.py",
                        "children": [
                            make_edge_node("c1"),
                            make_edge_node("c1"),
                        ],
                    },
                ],
            },
        ),
        (
            {
                "results": [
                    make_result("c1", "a/b.py"),
                    make_result("c2", "a/b.py"),
                ],
            },
            {
                "name": "a",
                "children": [
                    {
                        "name": "b.py",
                        "children": [
                            make_edge_node("c1"),
                            make_edge_node("c2"),
                        ],
                    },
                ],
            },
        ),
        (
            {
                "results": [
                    make_result("c1", "a.py"),
                ],
            },
            {
                "name": "a.py",
                "children": [make_edge_node("c1")],
            },
        ),
        (
            {
                "results": [
                    make_result("c1", "a/b/c/d/e.py"),
                    make_result("c1", "a/b/f.py"),
                    make_result("c1", "a/b/c/g/h.py"),
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
                                            {
                                                "name": "e.py",
                                                "children": [make_edge_node("c1")],
                                            },
                                        ],
                                    },
                                    {
                                        "name": "g",
                                        "children": [
                                            {
                                                "name": "h.py",
                                                "children": [make_edge_node("c1")],
                                            },
                                        ],
                                    },
                                ],
                            },
                            {"name": "f.py", "children": [make_edge_node("c1")]},
                        ],
                    },
                ],
            },
        ),
        (
            {
                "results": [],
            },
            {},
        ),
    ],
)
def test_viz_basic(data, expected):
    input = io.StringIO(json.dumps(data))
    output = io.StringIO()
    template = io.StringIO(const.DEFAULT_TEMPLATE_KEY)
    args = argparse.Namespace(
        input=input, output=output, template=template, no_browser=True
    )

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
            make_result("c1", "a/b.py"),
            make_result("c1", "c/d.py"),
        ]
    }

    input = io.StringIO(json.dumps(data))
    output = io.StringIO()
    template = io.StringIO(const.DEFAULT_TEMPLATE_KEY)
    args = argparse.Namespace(
        input=input, output=output, template=template, no_browser=True
    )

    with pytest.raises(ValueError):
        commands.viz.main(args)
