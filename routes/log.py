import logging
import sys


def init_logging(stream=sys.stderr, level=logging.INFO):
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        stream=stream,
        level=level,
    )
