import json


def compact_dumps(data):
    return json.dumps(data, separators=(",", ":"))


def main(args):
    output_buff = args.template.read()
    data = compact_dumps({"foo": "bar", "baz": "qux"})
    output_buff = output_buff.replace("{SEMGREP_DATA}", data)

    args.output.write(output_buff)

    return 0
