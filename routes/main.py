import argparse
import logging
import sys

from routes import __version__
from routes import commands
from routes import rules
from routes import templates

logger = logging.getLogger(__name__)


def parse_args(args=None):
    p = argparse.ArgumentParser(
        description="Find web application HTTP route authn and authz security bugs in your code.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    p.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Set logging level to debug",
    )
    p.add_argument(
        "-V",
        "--version",
        action="version",
        version=__version__,
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
        "--browser",
        action="store_true",
        help="Open HTML output file in browser",
    )
    viz_parser.add_argument(
        "-c",
        "--codeql",
        action="store_true",
        help="Parse input file as CodeQL SARIF format",
    )
    viz_parser.add_argument(
        "--global",
        dest="_global",
        action="store_true",
        help="Expiremental: enable global security configuration detection",
    )

    return p.parse_args(args=args)


def main():
    args = parse_args()

    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        stream=sys.stderr,
        level=logging.DEBUG if args.verbose else logging.INFO,
    )

    command_dispatch = {"which": commands.which.main, "viz": commands.viz.main}
    command = command_dispatch.get(args.command)
    if command is None:
        logger.error(f"Command unavailable: {args.command}")
        return 1

    logger.info("Starting command %s", args.command)
    result = command(args)
    logger.info("Finished command %s", args.command)

    return result


if __name__ == "__main__":
    sys.exit(main())
