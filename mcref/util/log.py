import logging
import sys
from functools import wraps
from logging import Logger
from logging import StreamHandler
from logging.handlers import RotatingFileHandler

DEFAULT_FORMAT = "[%(asctime)s][pid:%(process)d][%(levelname)s][%(name)s] %(message)s"


def module_logger(name: str) -> Logger:
    return logging.getLogger(name)


def configure_logging(log_level, log_file, fmt=DEFAULT_FORMAT):
    logger = logging.getLogger()  # root
    logger.setLevel(log_level)
    formatter = logging.Formatter(fmt=fmt)
    handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=2) if log_file else StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def with_entry_log(l):
    def wrapper(f):
        @wraps(f)
        def logged(*args, **kwargs):
            l.info("\n===== Starting! =====")
            result = f(*args, **kwargs)
            l.info("\n===== Done! =====")
            return result

        return logged

    return wrapper


def tee_log(log_method, message):
    print(message)
    log_method(message)
