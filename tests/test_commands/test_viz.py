import argparse
import io
import json

import pytest

from routes import commands
from routes import const
from routes import types


def make_file(data, name):
    result = io.StringIO(data)
    result.name = name
    return result


def make_result(lines, path, metadata=None, metavars=None):
    if metadata is None:
        metadata = {}

    if metavars is None:
        metavars = {}
    
    return {
        "check_id": "test_check_id",
        "path": path,
        "extra": {"metadata": metadata, "metavars": metavars, "lines": lines},
        "start": {"line": 0},
    }


def make_edge_node(name, fill=const.DEFAULT_FILL_COLOR):
    return {"name": f"ln 0: {name}", "fill": fill, "title": name}


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
        (
            {
                "results": [
                    make_result(
                        "c1",
                        "a/b.py",
                        metadata={
                            "route-detect": {"type": types.ResultType.ROUTE.value}
                        },
                    ),
                    make_result(
                        "c2",
                        "a/c.py",
                        metadata={
                            "route-detect": {"type": types.ResultType.ROUTE.value}
                        },
                    ),
                    make_result(
                        "c3",
                        "a/d.py",
                        metadata={
                            "route-detect": {
                                "type": types.ResultType.GLOBAL.value,
                                "fill": "testfill",
                            }
                        },
                    ),
                ],
            },
            {
                "name": "a",
                "children": [
                    {
                        "name": "b.py",
                        "children": [make_edge_node("c1", fill="testfill")],
                    },
                    {
                        "name": "c.py",
                        "children": [make_edge_node("c2", fill="testfill")],
                    },
                ],
            },
        ),
    ],
)
def test_viz_basic(data, expected):
    input = make_file(json.dumps(data), "test_input")
    output = make_file("", "test_output")
    template = make_file(const.DEFAULT_TEMPLATE_KEY, "test_template")
    args = argparse.Namespace(
        input=input,
        output=output,
        template=template,
        browser=False,
        interprocedural=True,
        _global=True,
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

    input = make_file(json.dumps(data), "test_input")
    output = make_file("", "test_output")
    template = make_file(const.DEFAULT_TEMPLATE_KEY, "test_template")
    args = argparse.Namespace(
        input=input,
        output=output,
        template=template,
        browser=False,
        interprocedural=True,
        _global=True,
    )

    with pytest.raises(ValueError):
        commands.viz.main(args)

    input.close()
    output.close()
    template.close()
