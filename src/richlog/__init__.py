"""
RichLog - A powerful Python logging library with rich formatting

Example:
    >>> from richlog import get_rich_logger, LogFormat, DateFormat
    >>> logger = get_rich_logger("myapp", log_format=LogFormat.DETAILED)
    >>> logger.info("Application started")
"""

import logging

# Configuration
from richlog.config.settings import ConfigError, Settings, load_settings

# Core functionality
from richlog.core import DateFormat, LogFormat, get_rich_logger
from richlog.core.handlers import AsyncHandler, BufferedHandler, FileHandler, JSONHandler

# Shortcuts
from richlog.shortcuts import (
    configure_from_dict,
    setup_file_logger,
    setup_json_logger,
    setup_logger_with_preset,
)

# Utilities
from richlog.utils.context import log_context
from richlog.utils.decorators import log_errors, log_execution_time

# Re-export logging levels for convenience
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

__version__ = "0.2.0"

__all__ = [
    "CRITICAL",
    # Logging levels
    "DEBUG",
    "ERROR",
    "INFO",
    "WARNING",
    "AsyncHandler",
    "BufferedHandler",
    "ConfigError",
    "DateFormat",
    # Handlers
    "FileHandler",
    "JSONHandler",
    "LogFormat",
    # Configuration
    "Settings",
    # Version
    "__version__",
    "configure_from_dict",
    # Core
    "get_rich_logger",
    "load_settings",
    "log_context",
    "log_errors",
    # Utilities
    "log_execution_time",
    "setup_file_logger",
    "setup_json_logger",
    # Shortcuts
    "setup_logger_with_preset",
]
