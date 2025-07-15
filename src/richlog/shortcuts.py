"""
便利なショートカット関数
"""

import logging
from pathlib import Path
from typing import Any, Literal, Optional

from richlog.config.settings import load_settings
from richlog.core import DateFormat, LogFormat, get_rich_logger
from richlog.core.handlers import BufferedHandler, FileHandler, JSONHandler


def setup_rich_logger(
    name: str = "app",
    *,
    config_file: Optional[Path] = None,
    preset: Literal["development", "production", "testing"] = "development",
    **kwargs: Any,
) -> logging.Logger:
    """簡単なセットアップ関数

    Args:
        name: ロガー名
        config_file: 設定ファイルのパス（オプション）
        preset: プリセット設定（development, production, testing）
        **kwargs: get_rich_loggerに渡す追加の引数

    Returns:
        設定されたロガー

    Example:
        >>> logger = setup_rich_logger("myapp", preset="production")
        >>> logger.info("Application started")
    """
    # プリセット設定
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

    # 設定ファイルから読み込み
    if config_file:
        settings = load_settings(config_file)
        return settings.create_logger(name)

    # プリセット設定を適用
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
    """ファイル出力を含むロガーを簡単にセットアップ

    Args:
        name: ロガー名
        filename: ログファイル名
        max_bytes: ファイルの最大サイズ（バイト）
        backup_count: バックアップファイルの数
        level: ログレベル
        log_format: ログフォーマット
        date_format: 日付フォーマット

    Returns:
        設定されたロガー
    """
    logger = get_rich_logger(
        name,
        level=level,
        log_format=log_format,
        date_format=date_format,
    )

    # ファイルハンドラーを追加
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
    """JSON形式のログを出力するロガーをセットアップ

    Args:
        name: ロガー名
        level: ログレベル
        include_console: コンソール出力も含めるか
        buffered: バッファリングを使用するか
        buffer_size: バッファサイズ

    Returns:
        設定されたロガー
    """
    if include_console:
        logger = get_rich_logger(name, level=level)
    else:
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.handlers.clear()

    # JSONハンドラーを作成
    json_handler = JSONHandler()
    json_handler.setLevel(level)

    # バッファリングを使用する場合
    if buffered:
        handler = BufferedHandler(json_handler, buffer_size=buffer_size)
    else:
        handler = json_handler

    logger.addHandler(handler)
    return logger


def configure_from_dict(config: dict[str, Any]) -> None:
    """辞書形式の設定から全体のログ設定を行う

    Args:
        config: ログ設定の辞書

    Example:
        >>> config = {
        ...     "version": 1,
        ...     "disable_existing_loggers": False,
        ...     "loggers": {
        ...         "myapp": {
        ...             "level": "DEBUG",
        ...             "handlers": ["console", "file"],
        ...         }
        ...     }
        ... }
        >>> configure_from_dict(config)
    """
    import logging.config

    # richlogハンドラーを登録
    if "handlers" in config:
        for handler_name, handler_config in config["handlers"].items():
            if handler_config.get("class") == "richlog.RichHandler":
                handler_config["class"] = "rich.logging.RichHandler"

    logging.config.dictConfig(config)
