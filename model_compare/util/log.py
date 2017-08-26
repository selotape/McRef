import logging
import sys
from functools import wraps
from logging import FileHandler, StreamHandler

DEFAULT_FORMAT = "[%(asctime)s][%(levelname)s][%(process)d][%(name)s] %(message)s"


def module_logger(name):
    return logging.getLogger(name)


def configure_logging(log_level, log_file):
    logger = logging.getLogger()  # root
    logger.setLevel(log_level)
    formatter = logging.Formatter(fmt=DEFAULT_FORMAT)
    if log_file:
        file_handler = FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        print("See log in '%s'\n" % log_file)
    else:
        stdout_handler = StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        logger.addHandler(stdout_handler)


def with_entry_log(l):
    def wrapper(f):
        @wraps(f)
        def logged(*args, **kwargs):
            l.info("===== Starting! =====")
            result = f(*args, **kwargs)
            l.info("===== Done! =====")
            return result

        return logged

    return wrapper


def tee_log(log_method, message):
    print(message)
    log_method(message)
