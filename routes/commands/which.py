import logging

from routes import rules

logger = logging.getLogger(__name__)


def main(args):
    logger.info("Printing rule path for %s", args.rule)
    print(rules.ALL_RULES[args.rule], end="")
    return 0
