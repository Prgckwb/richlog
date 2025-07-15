import logging
from unittest.mock import Mock

import pytest

from richlog.utils.context import log_context


class TestLogContext:
    def test_temporarily_changes_log_level(self) -> None:
        # ロガーをモック
        mock_logger = Mock()
        mock_logger.level = logging.INFO

        with log_context(logger=mock_logger, level=logging.DEBUG):
            # コンテキスト内ではDEBUGレベル
            assert mock_logger.setLevel.call_args_list[-1][0][0] == logging.DEBUG

        # コンテキストを出たら元のレベルに戻る
        assert mock_logger.setLevel.call_args_list[-1][0][0] == logging.INFO

    def test_restores_original_level_on_exception(self) -> None:
        mock_logger = Mock()
        mock_logger.level = logging.WARNING

        with pytest.raises(ValueError):
            with log_context(logger=mock_logger, level=logging.ERROR):
                # コンテキスト内でERRORレベル
                assert mock_logger.setLevel.call_args_list[-1][0][0] == logging.ERROR
                raise ValueError("Test error")

        # 例外が発生しても元のレベルに戻る
        assert mock_logger.setLevel.call_args_list[-1][0][0] == logging.WARNING

    def test_works_with_string_logger_name(self) -> None:
        # 実際のロガーを使ってテスト
        logger_name = "test_context_logger"
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)

        with log_context(logger=logger_name, level=logging.DEBUG):
            # コンテキスト内ではDEBUGレベル
            assert logger.level == logging.DEBUG

        # コンテキストを出たら元のレベルに戻る
        assert logger.level == logging.INFO

    def test_accepts_logger_instance(self) -> None:
        logger = logging.getLogger("test_logger_instance")
        logger.setLevel(logging.ERROR)

        with log_context(logger=logger, level=logging.INFO):
            assert logger.level == logging.INFO

        assert logger.level == logging.ERROR

    def test_nested_contexts(self) -> None:
        # 実際のロガーを使ってネストをテスト
        logger = logging.getLogger("test_nested_logger")
        logger.setLevel(logging.WARNING)

        with log_context(logger=logger, level=logging.INFO):
            # 最初のコンテキスト
            assert logger.level == logging.INFO
            original_in_first_context = logger.level

            with log_context(logger=logger, level=logging.DEBUG):
                # ネストしたコンテキスト
                assert logger.level == logging.DEBUG

            # 内側のコンテキストを出たら、内側が記録した「元のレベル」に戻る
            # (これはINFOになる)
            assert logger.level == original_in_first_context

        # 外側のコンテキストも出たら元のWARNINGに戻る
        assert logger.level == logging.WARNING
