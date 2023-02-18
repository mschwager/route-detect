import argparse
import logging
import sys

from routes import commands
from routes import log
from routes import rules
from routes import templates

logger = logging.getLogger(__name__)


def parse_args(args=None):
    p = argparse.ArgumentParser(
        description="TODO",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    p.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Set logging level to debug",
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
    viz_parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Do not open HTML output file in browser",
    )

    return p.parse_args(args=args)


def main():
    args = parse_args()

    log.init_logging(level=logging.DEBUG if args.verbose else logging.INFO)

    command_dispatch = {"which": commands.which.main, "viz": commands.viz.main}
    command = command_dispatch.get(args.command)
    if command is None:
        print(f"Command unavailable: {args.command}")
        return 1

    logger.info("Starting command %s", args.command)
    result = command(args)
    logger.info("Finished command %s", args.command)

    return result


if __name__ == "__main__":
    sys.exit(main())
