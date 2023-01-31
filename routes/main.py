import argparse

from routes import commands
from routes import rules
from routes import templates


def parse_args(args=None):
    p = argparse.ArgumentParser(
        description="TODO",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    subparsers = p.add_subparsers(dest="command", help="Command help")

    which_parser = subparsers.add_parser(
        "which", help="Output path of supported Semgrep rule"
    )
    which_parser.add_argument(
        "rule", choices=list(rules.ALL_RULES.keys()), help="Semgrep rule"
    )

    viz_parser = subparsers.add_parser("viz", help="Route visualization tool")
    viz_parser.add_argument(
        "input",
        action="store",
        type=argparse.FileType("r"),
        help="Semgrep JSON output file",
    )
    viz_parser.add_argument(
        "-o",
        "--output",
        action="store",
        default=templates.ROUTES_HTML,
        type=argparse.FileType("w"),
        help="Routes HTML output file",
    )
    viz_parser.add_argument(
        "-t",
        "--template",
        action="store",
        default=str(templates.ROUTES_HTML_TEMPLATE),
        type=argparse.FileType("r"),
        help="Routes HTML template file",
    )

    return p.parse_args(args=args)


def main():
    args = parse_args()

    command_dispatch = {"which": commands.which.main, "viz": commands.viz.main}
    command = command_dispatch.get(args.command)
    if command is None:
        print(f"Command unavailable: {args.command}")
        return 1

    return command(args)


if __name__ == "__main__":
    main()
