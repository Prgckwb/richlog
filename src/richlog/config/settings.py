import configparser
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    import tomllib
except ImportError:
    # Python 3.10以前の場合
    import tomli as tomllib  # type: ignore

from richlog.config.defaults import (
    DEFAULT_DATE_FORMAT,
    DEFAULT_LEVEL,
    DEFAULT_LOG_FORMAT,
    DEFAULT_RICH_TRACEBACKS,
    DEFAULT_TRACEBACK_SUPPRESS,
)


@dataclass
class Settings:
    level: str = DEFAULT_LEVEL
    format: str = DEFAULT_LOG_FORMAT
    date_format: str = DEFAULT_DATE_FORMAT
    rich_tracebacks: bool = DEFAULT_RICH_TRACEBACKS
    traceback_suppress: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        # traceback_suppressのデフォルト値を設定
        if not self.traceback_suppress:
            self.traceback_suppress = DEFAULT_TRACEBACK_SUPPRESS.copy()

    def get_log_level(self) -> int:
        """文字列のログレベルを logging モジュールの定数に変換"""
        level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        return level_map.get(self.level.upper(), logging.INFO)


def load_settings(config_path: Optional[Path] = None) -> Settings:
    """設定をファイルと環境変数から読み込む

    優先順位:
    1. 環境変数
    2. 設定ファイル(指定されている場合)
    3. デフォルト値
    """
    settings = Settings()

    # 設定ファイルから読み込み
    if config_path and config_path.exists():
        if config_path.suffix == ".toml":
            _load_from_toml(config_path, settings)
        else:
            _load_from_ini(config_path, settings)

    # 環境変数から読み込み(ファイル設定を上書き)
    _load_from_env(settings)

    return settings


def _load_from_toml(config_path: Path, settings: Settings) -> None:
    """TOMLファイルから設定を読み込む"""
    with open(config_path, "rb") as f:
        data = tomllib.load(f)

    if "richlog" in data:
        config = data["richlog"]
        settings.level = config.get("level", settings.level)
        settings.format = config.get("format", settings.format)
        settings.date_format = config.get("date_format", settings.date_format)
        settings.rich_tracebacks = config.get("rich_tracebacks", settings.rich_tracebacks)
        if "traceback_suppress" in config:
            settings.traceback_suppress = config["traceback_suppress"]


def _load_from_ini(config_path: Path, settings: Settings) -> None:
    """INIファイルから設定を読み込む"""
    config = configparser.ConfigParser()
    config.read(config_path)

    if "richlog" in config:
        section = config["richlog"]
        settings.level = section.get("level", settings.level)
        settings.format = section.get("format", settings.format)
        settings.date_format = section.get("date_format", settings.date_format)
        settings.rich_tracebacks = section.getboolean("rich_tracebacks", settings.rich_tracebacks)
        if "traceback_suppress" in section:
            # カンマ区切りの文字列をリストに変換
            suppress_str = section.get("traceback_suppress", "")
            settings.traceback_suppress = [s.strip() for s in suppress_str.split(",") if s.strip()]


def _load_from_env(settings: Settings) -> None:
    """環境変数から設定を読み込む"""
    settings.level = os.getenv("RICHLOG_LEVEL", settings.level)
    settings.format = os.getenv("RICHLOG_FORMAT", settings.format)
    settings.date_format = os.getenv("RICHLOG_DATE_FORMAT", settings.date_format)

    # ブール値の処理
    tracebacks_env = os.getenv("RICHLOG_RICH_TRACEBACKS")
    if tracebacks_env is not None:
        settings.rich_tracebacks = tracebacks_env.lower() in ("true", "1", "yes", "on")

    # リストの処理
    suppress_env = os.getenv("RICHLOG_TRACEBACK_SUPPRESS")
    if suppress_env:
        settings.traceback_suppress = [s.strip() for s in suppress_env.split(",") if s.strip()]
