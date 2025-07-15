"""
Convenient shortcut functions for setting up rich loggers.

This module provides high-level APIs for quickly configuring loggers
with sensible defaults and preset configurations.
"""

import logging
from pathlib import Path
from typing import Any, Literal, Optional

from richlog.config.settings import load_settings
from richlog.core import DateFormat, LogFormat, get_rich_logger
from richlog.core.handlers import BufferedHandler, FileHandler, JSONHandler


def setup_logger_with_preset(
    name: str = "app",
    *,
    config_file: Optional[Path] = None,
    preset: Literal["development", "production", "testing"] = "development",
    **kwargs: Any,
) -> logging.Logger:
    """Set up a logger with convenient preset configurations.

    This is a high-level function that simplifies logger setup by providing
    three preset configurations suitable for different environments:
    - development: DEBUG level, detailed format, rich tracebacks enabled
    - production: INFO level, verbose format, rich tracebacks disabled
    - testing: DEBUG level, simple format, rich tracebacks enabled

    Args:
        name: The name of the logger. Defaults to "app".
        config_file: Optional path to a configuration file. If provided,
            settings will be loaded from this file instead of using presets.
        preset: The preset configuration to use. Choose from:
            - "development": For local development with detailed debugging
            - "production": For production environments with structured logs
            - "testing": For test environments with minimal formatting
        **kwargs: Additional keyword arguments passed to get_rich_logger().
            These will override preset values.

    Returns:
        logging.Logger: A configured logger instance with Rich handler.

    Example:
        >>> # Quick setup for production
        >>> logger = setup_logger_with_preset("myapp", preset="production")
        >>> logger.info("Application started")

        >>> # Override preset values
        >>> logger = setup_logger_with_preset(
        ...     "myapp",
        ...     preset="development",
        ...     level=logging.WARNING  # Override DEBUG level
        ... )
    """
    # Preset configurations
    presets = {
        "development": {
            "level": logging.DEBUG,
            "log_format": LogFormat.DETAILED,
            "date_format": DateFormat.DEFAULT,
            "rich_tracebacks": True,
        },
        "production": {
            "level": logging.INFO,
            "log_format": LogFormat.VERBOSE,
            "date_format": DateFormat.ISO8601,
            "rich_tracebacks": False,
        },
        "testing": {
            "level": logging.DEBUG,
            "log_format": LogFormat.SIMPLE,
            "date_format": DateFormat.NOTHING,
            "rich_tracebacks": True,
        },
    }

    # Load from configuration file if provided
    if config_file:
        settings = load_settings(config_file)
        return settings.create_logger(name)

    # Apply preset configuration with any overrides
    preset_config = presets[preset].copy()
    preset_config.update(kwargs)

    return get_rich_logger(name, **preset_config)


def setup_file_logger(
    name: str = "app",
    filename: str = "app.log",
    *,
    max_bytes: int = 10_000_000,  # 10MB
    backup_count: int = 5,
    level: int = logging.INFO,
    log_format: LogFormat = LogFormat.DETAILED,
    date_format: DateFormat = DateFormat.ISO8601,
) -> logging.Logger:
    """Set up a logger with both console and file output.

    This function creates a logger that outputs to both the console (with Rich
    formatting) and a rotating file. The file handler automatically rotates
    when it reaches the specified size limit.

    Args:
        name: The name of the logger. Defaults to "app".
        filename: The name of the log file. Defaults to "app.log".
        max_bytes: Maximum size of a single log file in bytes before rotation.
            Defaults to 10MB (10,000,000 bytes).
        backup_count: Number of backup files to keep. When this limit is reached,
            the oldest file is deleted. Defaults to 5.
        level: The logging level (e.g., logging.INFO, logging.DEBUG).
            Defaults to logging.INFO.
        log_format: The format for log messages. Use LogFormat enum values.
            Defaults to LogFormat.DETAILED.
        date_format: The format for timestamps. Use DateFormat enum values.
            Defaults to DateFormat.ISO8601.

    Returns:
        logging.Logger: A configured logger with both console and file handlers.

    Example:
        >>> logger = setup_file_logger(
        ...     "myapp",
        ...     "myapp.log",
        ...     max_bytes=5_000_000,  # 5MB per file
        ...     backup_count=10,      # Keep 10 backup files
        ...     level=logging.DEBUG
        ... )
        >>> logger.info("This appears in both console and file")
    """
    logger = get_rich_logger(
        name,
        level=level,
        log_format=log_format,
        date_format=date_format,
    )

    # Add file handler with rotation
    file_handler = FileHandler(
        filename,
        max_bytes=max_bytes,
        backup_count=backup_count,
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))
    logger.addHandler(file_handler)

    return logger


def setup_json_logger(
    name: str = "app",
    *,
    level: int = logging.INFO,
    include_console: bool = True,
    buffered: bool = False,
    buffer_size: int = 100,
) -> logging.Logger:
    """Set up a logger that outputs logs in JSON format.

    This function creates a logger optimized for structured logging,
    outputting each log entry as a JSON object. This is particularly
    useful for log aggregation systems and automated log analysis.

    Args:
        name: The name of the logger. Defaults to "app".
        level: The logging level (e.g., logging.INFO, logging.DEBUG).
            Defaults to logging.INFO.
        include_console: Whether to also include Rich console output
            alongside JSON output. Defaults to True.
        buffered: Whether to use buffering for performance. When True,
            logs are collected in memory and flushed periodically.
            Defaults to False.
        buffer_size: Number of log entries to buffer before flushing.
            Only used when buffered=True. Defaults to 100.

    Returns:
        logging.Logger: A configured logger with JSON output capability.

    Example:
        >>> # JSON output with console display
        >>> logger = setup_json_logger("myapp", include_console=True)
        >>> logger.info("User login", extra={"user_id": 123, "ip": "192.168.1.1"})

        >>> # JSON only for production systems
        >>> logger = setup_json_logger(
        ...     "myapp",
        ...     include_console=False,
        ...     buffered=True,
        ...     buffer_size=500
        ... )
    """
    if include_console:
        logger = get_rich_logger(name, level=level)
    else:
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.handlers.clear()

    # Create JSON handler
    json_handler = JSONHandler()
    json_handler.setLevel(level)

    # Use buffering if requested
    if buffered:
        handler = BufferedHandler(json_handler, buffer_size=buffer_size)
    else:
        handler = json_handler

    logger.addHandler(handler)
    return logger


def configure_from_dict(config: dict[str, Any]) -> None:
    """Configure logging from a dictionary configuration.

    This function provides compatibility with Python's standard
    logging.config.dictConfig() while adding support for richlog
    handlers. It's useful when you need to configure multiple
    loggers with complex hierarchies.

    Args:
        config: A dictionary containing the logging configuration.
            Should follow the schema defined in Python's logging.config
            documentation. Special support is added for richlog handlers.

    Example:
        >>> config = {
        ...     "version": 1,
        ...     "disable_existing_loggers": False,
        ...     "formatters": {
        ...         "detailed": {
        ...             "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        ...         }
        ...     },
        ...     "handlers": {
        ...         "console": {
        ...             "class": "richlog.RichHandler",
        ...             "level": "DEBUG",
        ...             "formatter": "detailed"
        ...         },
        ...         "file": {
        ...             "class": "logging.FileHandler",
        ...             "filename": "app.log",
        ...             "level": "INFO",
        ...             "formatter": "detailed"
        ...         }
        ...     },
        ...     "loggers": {
        ...         "myapp": {
        ...             "level": "DEBUG",
        ...             "handlers": ["console", "file"],
        ...             "propagate": False
        ...         }
        ...     }
        ... }
        >>> configure_from_dict(config)
    """
    import logging.config

    # Register richlog handlers for compatibility
    if "handlers" in config:
        for _handler_name, handler_config in config["handlers"].items():
            if handler_config.get("class") == "richlog.RichHandler":
                handler_config["class"] = "rich.logging.RichHandler"

    logging.config.dictConfig(config)
