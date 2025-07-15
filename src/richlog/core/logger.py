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
    """Create a logger with Rich console handler.

    This is the core function for creating loggers with Rich formatting.
    It provides direct control over all logging parameters without any
    preset configurations. Use this when you need fine-grained control
    over your logger setup.

    Args:
        name: The name of the logger. Defaults to __name__ to use the
            current module's name.
        level: The logging level (e.g., logging.INFO, logging.DEBUG).
            Defaults to logging.INFO.
        rich_tracebacks: Whether to enable Rich's enhanced traceback
            formatting with syntax highlighting and better structure.
            Defaults to True.
        traceback_suppress: List of module names to suppress in tracebacks.
            Useful for hiding framework internals. Defaults to None.
        log_format: The format string for log messages. Can be either a
            string format or a LogFormat enum value. Defaults to
            LogFormat.DEFAULT.
        date_format: The format string for timestamps. Can be either a
            string format or a DateFormat enum value. Defaults to
            DateFormat.DEFAULT.

    Returns:
        logging.Logger: A configured logger with Rich console handler.

    Example:
        >>> # Basic usage with defaults
        >>> logger = get_rich_logger("myapp")
        >>> logger.info("Application started")

        >>> # Custom configuration
        >>> logger = get_rich_logger(
        ...     "myapp.database",
        ...     level=logging.DEBUG,
        ...     rich_tracebacks=True,
        ...     traceback_suppress=["sqlalchemy", "urllib3"],
        ...     log_format=LogFormat.DETAILED,
        ...     date_format="%H:%M:%S"
        ... )
        >>> logger.debug("Database query executed")
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Clear existing handlers to prevent duplication
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
