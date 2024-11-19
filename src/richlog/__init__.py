import logging
from dataclasses import dataclass
from typing import Optional, List, Union

from rich.logging import RichHandler

DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL


@dataclass(frozen=True)
class LogFormat:
    DEFAULT: str = "%(message)s"
    VERBOSE: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    SIMPLE: str = "%(levelname)s: %(message)s"
    DETAILED: str = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
    NOTHING: str = ""


@dataclass(frozen=True)
class DateFormat:
    DEFAULT: str = "%Y-%m-%d %H:%M:%S"
    ISO8601: str = "%Y-%m-%dT%H:%M:%S"
    US: str = "%m/%d/%Y %I:%M:%S %p"
    EU: str = "%d/%m/%Y %H:%M:%S"
    NOTHING: str = ""


def get_rich_logger(
    name: str = __name__,
    *,
    level: int = INFO,
    rich_tracebacks: bool = True,
    traceback_suppress: Optional[List] = None,
    log_format: Union[str, LogFormat] = LogFormat.DEFAULT,
    date_format: Union[str, DateFormat] = DateFormat.DEFAULT,
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Clear existing handlers to ensure no duplicates
    if logger.hasHandlers():
        logger.handlers.clear()

    handler = RichHandler(
        show_time=True,
        show_level=True,
        show_path=True,
        enable_link_path=True,
        rich_tracebacks=rich_tracebacks,
        tracebacks_suppress=traceback_suppress or [],
    )
    handler.setLevel(level)

    formatter = logging.Formatter(log_format, datefmt=date_format)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger
