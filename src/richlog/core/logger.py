import logging
from typing import Optional, Union

from rich.logging import RichHandler

from richlog.core.formatters import DateFormat, LogFormat


def get_rich_logger(
    name: str = __name__,
    *,
    level: int = logging.INFO,
    rich_tracebacks: bool = True,
    traceback_suppress: Optional[list[str]] = None,
    log_format: Union[str, LogFormat] = LogFormat.DEFAULT,
    date_format: Union[str, DateFormat] = DateFormat.DEFAULT,
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 既存のハンドラーをクリアして重複を防ぐ
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
