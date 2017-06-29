import logging
import sys
from logging import FileHandler, StreamHandler


class LoggingMixin(object):
    def __init__(self):
        self.logger = class_logger(self)


def module_logger(module_name):
    # type: (basestring) -> logging.Logger
    return logging.getLogger(module_name)


def class_logger(cls_or_instance):
    # type: (...) -> logging.Logger
    cls = cls_or_instance if isinstance(cls_or_instance, type) else type(cls_or_instance)
    return module_logger(cls.__module__).getChild(cls.__name__)


DEFAULT_FORMAT = "[%(asctime)s][%(levelname)s][%(name)s] %(message)s"


def configure_logging(log_level, log_file):
    logger = logging.getLogger()  # root
    logger.setLevel(log_level)
    formatter = logging.Formatter(fmt=DEFAULT_FORMAT)
    if log_file:
        file_handler = FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    stdout_handler = StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)


def with_entry_log(logger):
    def wrap(f):
        def wrapped_f(*args):
            logger.debug("entered {} with args {}".format(f.__name__, args))
            f(*args)
            logger.debug("exited  {}".format(f.__name__))

        return wrapped_f

    return wrap
