import logging
import sys
from functools import wraps
from logging import FileHandler, StreamHandler

DEFAULT_FORMAT = "[%(asctime)s][pid:%(process)d][%(levelname)s][%(name)s] %(message)s"


def module_logger(name):
    return logging.getLogger(name)


def configure_logging(log_level, log_file, fmt=DEFAULT_FORMAT):
    logger = logging.getLogger()  # root
    logger.setLevel(log_level)
    formatter = logging.Formatter(fmt=fmt)
    handler = FileHandler(log_file) if log_file else StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def with_entry_log(l):
    def wrapper(f):
        @wraps(f)
        def logged(*args, **kwargs):
            l.info("\n===== Starting! =====")
            result = f(*args, **kwargs)
            l.info("===== Done! =====\n")
            return result

        return logged

    return wrapper


def tee_log(log_method, message):
    print(message)
    log_method(message)
