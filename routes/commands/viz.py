import collections
import json
import logging
import pathlib
import re
import webbrowser

from routes import const
from routes import types
from routes import util

logger = logging.getLogger(__name__)

RAIL_SYMBOL_RE = re.compile(r":(?P<name>[a-z_]+)")
RAIL_CONTROLLER_RE = re.compile(r"(?P<controller>[a-z_]+)#(?P<action>[a-z_]+)")


def rails_route_to_controller(result):
    content = result.metavar_content(result.rd_connect_on)

    # Symbol route, e.g. ":user"
    symbol_match = re.match(RAIL_SYMBOL_RE, content)
    if symbol_match is not None:
        return util.pascal_case(symbol_match.group("name")) + "Controller"

    # Controller name, e.g. "user#action"
    controller_match = re.search(RAIL_CONTROLLER_RE, content)
    if controller_match is not None:
        return util.pascal_case(controller_match.group("controller")) + "Controller"

    # Else try content itself even though it's unlikely to work
    return content


NORMALIZERS = {types.Framework.RAILS.value: rails_route_to_controller}


def get_connectors(connector_results):
    def connector_key(result):
        return result.metavar_content(result.rd_connect_on)

    results = {}
    for key, group in util.sorted_groupby(connector_results, key=connector_key):
        group_list = list(group)
        if len(group_list) > 1:
            logger.warning("Grouping on %s is ambiguous", key)
            continue
        results[key] = group_list[0]

    return results


def d3ify(parts, output, result, connectors):
    part = parts.pop(0)

    new_node = {"name": part}

    if parts:
        new_output = []
        new_node["children"] = new_output
        d3ify(parts, new_output, result, connectors)
    else:
        name = f"ln {result.start_line}: {result.first_line}"

        if result.rd_normalizer:
            normalizer = NORMALIZERS.get(result.rd_normalizer)
            normalized = normalizer(result)
            connector = connectors.get(normalized)
            fill = connector.rd_fill if connector else result.rd_fill
        else:
            fill = result.rd_fill

        check_node = {"name": name, "fill": fill}
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
    logger.info("Reading input file %s", args.input.name)
    data = json.load(args.input)

    semgrep_results = [types.SemgrepResult(r) for r in data["results"]]
    counts = collections.Counter([r.check_id for r in semgrep_results])
    count_output = " ".join(f"{k}={v}" for k, v in counts.items())
    logger.info("Finding rule counts: %s", count_output)

    results_by_type = {
        key: list(group)
        for key, group in util.sorted_groupby(semgrep_results, key=lambda r: r.rd_type)
    }

    connector_results = results_by_type.get(types.ResultType.CONNECTOR.value, {})
    connectors = get_connectors(connector_results)

    root_paths = set()
    d3_results = []
    for result in results_by_type.get(types.ResultType.ROUTE.value, []):
        path = pathlib.PurePath(result.path)
        logger.debug("Processing %s %s %s", result.check_id, path, result.start_line)
        root, *_ = path.parts
        root_paths.add(root)
        output = []
        d3ify(list(path.parts), output, result, connectors)
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

    if not args.no_browser:
        logger.info("Opening output file in browser")
        output_uri = pathlib.Path(args.output.name).resolve().as_uri()
        webbrowser.open(output_uri)

    return 0 if success else 1
