import logging
from collections.abc import Generator
from contextlib import contextmanager
from typing import Union


@contextmanager
def log_context(
    logger: Union[str, logging.Logger],
    level: int,
) -> Generator[None, None, None]:
    """Context manager to temporarily change log level.

    Args:
        logger: Logger name or logger instance
        level: Log level to set

    Yields:
        None

    Example:
        >>> with log_context("myapp", logging.DEBUG):
        ...     # Logs are output at DEBUG level within this block
        ...     logger.debug("Debug message")
    """
    # Get logger instance
    if isinstance(logger, str):
        logger_instance = logging.getLogger(logger)
    else:
        logger_instance = logger

    # Save original level
    original_level = logger_instance.level

    try:
        # Set new level
        logger_instance.setLevel(level)
        yield
    finally:
        # Restore original level
        logger_instance.setLevel(original_level)
