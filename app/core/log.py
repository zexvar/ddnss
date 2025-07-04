import logging
import sys

from flask import Flask
from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(level, record.getMessage())


def register_log_handler(app: Flask):
    sys.tracebacklimit = 5
    level = logging.DEBUG if app.debug else logging.INFO

    # Register loguru to handle Flask's logger
    app.logger.addHandler(InterceptHandler())
    app.logger.setLevel(level)

    # Redirect std logging to loguru
    logging.basicConfig(handlers=[InterceptHandler()], level=level, force=True)
