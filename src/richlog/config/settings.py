import configparser
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    import tomllib
except ImportError:
    # For Python 3.10 and earlier
    import tomli as tomllib  # type: ignore

from richlog.config.defaults import (
    DEFAULT_DATE_FORMAT,
    DEFAULT_LEVEL,
    DEFAULT_LOG_FORMAT,
    DEFAULT_RICH_TRACEBACKS,
    DEFAULT_TRACEBACK_SUPPRESS,
)
from richlog.core import get_rich_logger
from richlog.core.formatters import DateFormat, LogFormat


class ConfigError(Exception):
    """Configuration error"""

    pass


@dataclass
class Settings:
    level: str = DEFAULT_LEVEL
    format: str = DEFAULT_LOG_FORMAT
    date_format: str = DEFAULT_DATE_FORMAT
    rich_tracebacks: bool = DEFAULT_RICH_TRACEBACKS
    traceback_suppress: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        # Set default value for traceback_suppress
        if not self.traceback_suppress:
            self.traceback_suppress = DEFAULT_TRACEBACK_SUPPRESS.copy()

    def _validate_log_level(self, raise_on_invalid: bool = True) -> bool:
        """Validate log level

        Args:
            raise_on_invalid: If True, raise ConfigError on invalid level.
                            If False, return False on invalid level.

        Returns:
            True if valid, False if invalid (when raise_on_invalid=False)
        """
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if self.level.upper() not in valid_levels:
            if raise_on_invalid:
                raise ConfigError(
                    f"Invalid log level: {self.level}. "
                    f"Valid levels are: {', '.join(sorted(valid_levels))}"
                )
            return False
        return True

    def get_log_level(self) -> int:
        """Convert string log level to logging module constant"""
        level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        # Return default INFO level for invalid levels
        if not self._validate_log_level(raise_on_invalid=False):
            return logging.INFO
        return level_map.get(self.level.upper(), logging.INFO)

    def create_logger(self, name: str) -> logging.Logger:
        """Create logger based on settings"""
        # Convert format to Enum
        try:
            log_format = LogFormat.from_string(self.format)
        except ValueError:
            log_format = LogFormat.DEFAULT

        try:
            date_format = DateFormat.from_string(self.date_format)
        except ValueError:
            date_format = DateFormat.DEFAULT

        return get_rich_logger(
            name=name,
            level=self.get_log_level(),
            log_format=log_format,
            date_format=date_format,
            rich_tracebacks=self.rich_tracebacks,
            traceback_suppress=self.traceback_suppress,
        )


def load_settings(config_path: Optional[Path] = None) -> Settings:
    """Load settings from file and environment variables

    Priority order:
    1. Environment variables
    2. Configuration file (if specified)
    3. Default values
    """
    settings = Settings()

    # Load from configuration file
    if config_path:
        if not config_path.exists():
            raise ConfigError(f"Configuration file not found: {config_path}")

        try:
            if config_path.suffix == ".toml":
                _load_from_toml(config_path, settings)
            else:
                _load_from_ini(config_path, settings)
        except Exception as e:
            raise ConfigError(f"Failed to load configuration from {config_path}: {e}") from e

    # Load from environment variables (overrides file settings)
    try:
        _load_from_env(settings)
    except Exception as e:
        raise ConfigError(f"Failed to load configuration from environment: {e}") from e

    # Validate log level after all settings are loaded
    settings._validate_log_level(raise_on_invalid=True)

    return settings


def _load_from_toml(config_path: Path, settings: Settings) -> None:
    """Load settings from TOML file"""
    try:
        with open(config_path, "rb") as f:
            data = tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        raise ConfigError(f"Invalid TOML format: {e}") from e

    if "richlog" in data:
        config = data["richlog"]
        settings.level = config.get("level", settings.level)
        settings.format = config.get("format", settings.format)
        settings.date_format = config.get("date_format", settings.date_format)
        settings.rich_tracebacks = config.get("rich_tracebacks", settings.rich_tracebacks)
        if "traceback_suppress" in config:
            settings.traceback_suppress = config["traceback_suppress"]

        # Re-validate
        settings._validate_log_level()


def _load_from_ini(config_path: Path, settings: Settings) -> None:
    """Load settings from INI file"""
    config = configparser.ConfigParser()
    try:
        config.read(config_path)
    except configparser.Error as e:
        raise ConfigError(f"Invalid INI format: {e}") from e

    if "richlog" in config:
        section = config["richlog"]
        settings.level = section.get("level", settings.level)
        settings.format = section.get("format", settings.format)
        settings.date_format = section.get("date_format", settings.date_format)
        settings.rich_tracebacks = section.getboolean("rich_tracebacks", settings.rich_tracebacks)
        if "traceback_suppress" in section:
            # Convert comma-separated string to list
            suppress_str = section.get("traceback_suppress", "")
            settings.traceback_suppress = [s.strip() for s in suppress_str.split(",") if s.strip()]

        # Re-validate
        settings._validate_log_level()


def _load_from_env(settings: Settings) -> None:
    """Load settings from environment variables"""
    if level := os.getenv("RICHLOG_LEVEL"):
        settings.level = level
    if format_str := os.getenv("RICHLOG_FORMAT"):
        settings.format = format_str
    if date_format := os.getenv("RICHLOG_DATE_FORMAT"):
        settings.date_format = date_format

    # Handle boolean values
    tracebacks_env = os.getenv("RICHLOG_RICH_TRACEBACKS")
    if tracebacks_env is not None:
        settings.rich_tracebacks = tracebacks_env.lower() in ("true", "1", "yes", "on")

    # Handle list values
    suppress_env = os.getenv("RICHLOG_TRACEBACK_SUPPRESS")
    if suppress_env:
        settings.traceback_suppress = [s.strip() for s in suppress_env.split(",") if s.strip()]

    # 再検証
    settings._validate_log_level()
