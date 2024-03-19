import logging
import sys

from task_ops.exceptions import IllegalArgumentException


def bootstrap():
    pass


def get_logger(name: str, level=logging.DEBUG):
    if not name:
        raise IllegalArgumentException("'logger name' is required")
    log = logging.getLogger(name)
    log.setLevel(level)
    return log


# Fallback Configuration; Will be overridden in bootstrap
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
