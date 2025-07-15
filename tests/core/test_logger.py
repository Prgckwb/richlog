import logging
from unittest.mock import Mock, patch

from richlog.core.logger import get_rich_logger


class TestGetRichLogger:
    def test_creates_logger_with_name(self) -> None:
        logger = get_rich_logger("test_logger")
        assert logger.name == "test_logger"

    def test_creates_logger_with_default_name(self) -> None:
        logger = get_rich_logger()
        assert logger.name == "richlog.core.logger"

    def test_sets_correct_log_level(self) -> None:
        logger = get_rich_logger(level=logging.DEBUG)
        assert logger.level == logging.DEBUG

    def test_default_log_level_is_info(self) -> None:
        logger = get_rich_logger()
        assert logger.level == logging.INFO

    def test_logger_has_rich_handler(self) -> None:
        logger = get_rich_logger()
        assert len(logger.handlers) == 1
        handler = logger.handlers[0]
        assert handler.__class__.__name__ == "RichHandler"

    def test_clears_existing_handlers(self) -> None:
        logger = get_rich_logger("duplicate_test")
        initial_handler_count = len(logger.handlers)

        # 同じ名前でロガーを再作成
        logger = get_rich_logger("duplicate_test")
        assert len(logger.handlers) == initial_handler_count

    @patch("richlog.core.logger.RichHandler")
    def test_rich_handler_configuration(self, mock_rich_handler_class: Mock) -> None:
        mock_handler = Mock()
        mock_rich_handler_class.return_value = mock_handler

        get_rich_logger(
            name="config_test",
            level=logging.WARNING,
            rich_tracebacks=False,
            traceback_suppress=["module1", "module2"],
        )

        # RichHandlerが正しい引数で呼ばれたことを確認
        mock_rich_handler_class.assert_called_once_with(
            show_time=True,
            show_level=True,
            show_path=True,
            enable_link_path=True,
            rich_tracebacks=False,
            tracebacks_suppress=["module1", "module2"],
        )

        # ハンドラーのレベルが設定されたことを確認
        mock_handler.setLevel.assert_called_once_with(logging.WARNING)

    def test_formatter_is_set_correctly(self) -> None:
        logger = get_rich_logger(
            log_format="%(levelname)s: %(message)s",
            date_format="%Y-%m-%d",
        )
        handler = logger.handlers[0]
        formatter = handler.formatter

        # フォーマッターが設定されていることを確認
        assert formatter is not None
        assert formatter._fmt == "%(levelname)s: %(message)s"
        assert formatter.datefmt == "%Y-%m-%d"

    def test_accepts_string_log_format(self) -> None:
        custom_format = "%(asctime)s - %(message)s"
        logger = get_rich_logger(log_format=custom_format)
        handler = logger.handlers[0]
        assert handler.formatter._fmt == custom_format

    def test_accepts_string_date_format(self) -> None:
        custom_date_format = "%d/%m/%Y"
        logger = get_rich_logger(date_format=custom_date_format)
        handler = logger.handlers[0]
        assert handler.formatter.datefmt == custom_date_format
