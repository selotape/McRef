import logging
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


def configure_logging(conf):
    log_level, log_file = conf.get_log_conf()

    logger = logging.getLogger()  # root
    logger.setLevel(log_level)
    handler = FileHandler(log_file) if log_file else StreamHandler()
    handler.setFormatter(logging.Formatter(fmt=DEFAULT_FORMAT))
    logger.addHandler(handler)
