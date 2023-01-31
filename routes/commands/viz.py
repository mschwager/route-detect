import json


def compact_dumps(data):
    return json.dumps(data, separators=(",", ":"))


def main(args):
    output_buff = args.template.read()
    data = compact_dumps(json.load(args.input))
    output_buff = output_buff.replace("{SEMGREP_DATA}", data)

    written = args.output.write(output_buff)
    success = len(output_buff) == written

    return 0 if success else 1
