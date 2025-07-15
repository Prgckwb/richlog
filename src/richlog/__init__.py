"""
RichLog - A powerful Python logging library with rich formatting

Example:
    >>> from richlog import get_rich_logger, LogFormat, DateFormat
    >>> logger = get_rich_logger("myapp", log_format=LogFormat.DETAILED)
    >>> logger.info("Application started")
"""

import logging

# Core functionality
from richlog.core import DateFormat, LogFormat, get_rich_logger
from richlog.core.handlers import AsyncHandler, BufferedHandler, FileHandler, JSONHandler

# Configuration
from richlog.config.settings import ConfigError, Settings, load_settings

# Utilities
from richlog.utils.context import log_context
from richlog.utils.decorators import log_errors, log_execution_time

# Shortcuts
from richlog.shortcuts import (
    configure_from_dict,
    setup_file_logger,
    setup_json_logger,
    setup_rich_logger,
)

# Re-export logging levels for convenience
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

__version__ = "0.2.0"

__all__ = [
    # Version
    "__version__",
    # Core
    "get_rich_logger",
    "LogFormat",
    "DateFormat",
    # Handlers
    "FileHandler",
    "JSONHandler",
    "AsyncHandler",
    "BufferedHandler",
    # Configuration
    "Settings",
    "load_settings",
    "ConfigError",
    # Utilities
    "log_execution_time",
    "log_errors",
    "log_context",
    # Shortcuts
    "setup_rich_logger",
    "setup_file_logger",
    "setup_json_logger",
    "configure_from_dict",
    # Logging levels
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
]
