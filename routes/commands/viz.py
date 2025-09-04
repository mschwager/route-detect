import collections
import logging
import pathlib
import webbrowser

from routes import const
from routes import types
from routes import util

logger = logging.getLogger(__name__)


def get_global(global_results, _global):
    if not _global:
        return None

    global_locations = " ".join(
        f"{r.id}:{r.path}:{r.start_line}" for r in global_results
    )

    if len(global_results) > 1:
        logger.warning(
            "Multiple global configurations are ambiguous: %s", global_locations
        )
        return None
    elif len(global_results) == 0:
        logger.info("Found no global configuration")
        return None

    logger.info("Found global configuration: %s", global_locations)

    return global_results[0]


def d3ify(parts, output, result, _global):
    part = parts.pop(0)

    new_node = {"name": part}

    if parts:
        new_output = []
        new_node["children"] = new_output
        d3ify(parts, new_output, result, _global)
    else:
        name = f"ln {result.start_line}: {result.first_line}"
        fill = _global.rd_fill if _global else result.rd_fill
        check_node = {"name": name, "fill": fill, "title": result.lines}
        new_node.setdefault("children", []).append(check_node)

    output.append(new_node)


def merge_d3_results(d1s, d2s):
    for d2 in d2s:
        matching_d1 = next((d1 for d1 in d1s if d1["name"] == d2["name"]), None)
        if matching_d1 is None or "children" not in d2:
            d1s.append(d2)
        elif "children" in matching_d1 and "children" in d2:
            merge_d3_results(matching_d1["children"], d2["children"])


def main(args):
    logger.info("Processing input file %s", args.input.name)

    output_cls = types.CodeQLOutput if args.codeql else types.SemgrepOutput
    output = output_cls.from_fd(args.input)
    results = output.results

    for result_id, count in collections.Counter([r.id for r in results]).items():
        logger.info("Found %d results for id %s", count, result_id)

    results_by_type = {
        key: list(group)
        for key, group in util.sorted_groupby(results, key=lambda r: r.rd_type)
    }

    global_results = results_by_type.get(types.ResultType.GLOBAL.value, {})
    _global = get_global(global_results, args._global)

    root_paths = set()
    d3_results = []
    sorted_results = sorted(
        results_by_type.get(types.ResultType.ROUTE.value, []),
        key=lambda r: r.start_line,
    )
    for result in sorted_results:
        path = pathlib.PurePath(result.path)
        logger.debug("Processing %s:%s:%s", result.id, path, result.start_line)
        root, *_ = path.parts
        root_paths.add(root)
        output = []
        d3ify(list(path.parts), output, result, _global)
        d3_results.append(output)

    all_same_root = len(root_paths) == 1
    if root_paths and not all_same_root:
        raise ValueError(
            f"Tree assumes a common root ({root_paths}), please only specify a single directory"
        )

    d3_tree = []
    for d3_result in d3_results:
        merge_d3_results(d3_tree, d3_result)

    # Since all paths share the same root we can start our tree there
    d3_tree = d3_tree[0] if d3_tree else {}

    if not d3_tree:
        logging.error(
            "No results found, please ensure your framework is supported or "
            "file an issue at https://github.com/mschwager/route-detect/issues"
        )

    template_name = pathlib.PurePath(args.template.name).name
    logger.info("Formatting template %s", template_name)
    output_buff = args.template.read()
    template_data = util.compact_dumps(d3_tree)
    output_buff = output_buff.replace(const.DEFAULT_TEMPLATE_KEY, template_data)

    logger.info("Writing output file %s", args.output.name)
    written = args.output.write(output_buff)
    success = len(output_buff) == written

    if args.browser:
        logger.info("Opening output file in browser")
        output_uri = pathlib.Path(args.output.name).resolve().as_uri()
        webbrowser.open(output_uri)

    return 0 if success else 1
