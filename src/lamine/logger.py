import logging

from rich.logging import RichHandler


def set_logger():
    logger = logging.getLogger("logger")
    logger.setLevel(logging.DEBUG)
    c_handler = RichHandler(show_time=False, show_path=True)
    c_handler.setLevel(logging.DEBUG)
    logger.addHandler(c_handler)
    return logger


LOGGER = set_logger()
