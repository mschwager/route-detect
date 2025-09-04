import logging

from routes import queries
from routes import rules

logger = logging.getLogger(__name__)


def main(args):
    logger.info("Printing rule path for %s", args.rule)

    if args.codeql:
        path = queries.ALL_QUERIES.get(args.rule)
    else:
        path = rules.ALL_RULES.get(args.rule)

    if not path:
        tool = "CodeQL" if args.codeql else "Semgrep"
        logger.error("Framework %s does not support %s", args.rule, tool)
        return 1

    print(path, end="")

    return 0
