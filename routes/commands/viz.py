import json
import pathlib
import webbrowser

from routes import const


def compact_dumps(data):
    return json.dumps(data, separators=(",", ":"))


def d3ify(parts, output, result):
    part = parts.pop(0)

    new_node = {"name": part}

    if parts:
        new_output = []
        new_node["children"] = new_output
        d3ify(parts, new_output, result)
    else:
        check_id = result["check_id"]
        route_detect_metadata = result["extra"]["metadata"].get("route_detect", {})
        fill = route_detect_metadata.get("fill", const.DEFAULT_FILL_COLOR)
        check_node = {"name": check_id, "fill": fill}
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
    data = json.load(args.input)

    d3_results = []
    for result in data["results"]:
        path = pathlib.PurePath(result["path"])
        output = []
        d3ify(list(path.parts), output, result)
        d3_results.append(output)

    root_paths = [n[0]["name"] for n in d3_results if n]
    all_same_root = len(set(root_paths)) == 1
    if not all_same_root:
        raise ValueError(f"Broken invariant, different root paths: {root_paths}")

    d3_tree = []
    for d3_result in d3_results:
        merge_d3_results(d3_tree, d3_result)

    # Since all paths share the same root we can start our tree there
    d3_tree = d3_tree[0]

    output_buff = args.template.read()
    template_data = compact_dumps(d3_tree)
    output_buff = output_buff.replace(const.DEFAULT_TEMPLATE_KEY, template_data)

    written = args.output.write(output_buff)
    success = len(output_buff) == written

    if not args.no_browser:
        output_uri = pathlib.Path(args.output.name).resolve().as_uri()
        webbrowser.open(output_uri)

    return 0 if success else 1
