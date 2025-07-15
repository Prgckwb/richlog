import logging
from collections.abc import Generator
from contextlib import contextmanager
from typing import Union


@contextmanager
def log_context(
    logger: Union[str, logging.Logger],
    level: int,
) -> Generator[None, None, None]:
    """一時的にログレベルを変更するコンテキストマネージャー

    Args:
        logger: ロガー名またはロガーインスタンス
        level: 設定するログレベル

    Yields:
        None

    Example:
        >>> with log_context("myapp", logging.DEBUG):
        ...     # このブロック内ではDEBUGレベルでログが出力される
        ...     logger.debug("Debug message")
    """
    # ロガーインスタンスを取得
    if isinstance(logger, str):
        logger_instance = logging.getLogger(logger)
    else:
        logger_instance = logger

    # 元のレベルを保存
    original_level = logger_instance.level

    try:
        # 新しいレベルを設定
        logger_instance.setLevel(level)
        yield
    finally:
        # 元のレベルに戻す
        logger_instance.setLevel(original_level)
