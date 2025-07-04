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
    fromat = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> "
        "<level>{level:>7}</level> "
        "<green>{thread}</green> | "
        "<cyan>[{name:>18}:{line}]</cyan> : "
        "<level>{message}</level>"
    )
    logger.remove()
    logger.add(
        sys.stdout,
        format=fromat,
        level=level,
        backtrace=True,
        diagnose=False,
        enqueue=True,
    )

    # Register loguru to handle Flask's logger
    app.logger.addHandler(InterceptHandler())
    app.logger.setLevel(level)

    # Redirect std logging to loguru
    logging.basicConfig(handlers=[InterceptHandler()], level=level, force=True)
