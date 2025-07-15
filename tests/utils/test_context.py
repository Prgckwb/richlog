import logging
from unittest.mock import Mock

import pytest

from richlog.utils.context import log_context


class TestLogContext:
    def test_temporarily_changes_log_level(self) -> None:
        # Mock the logger
        mock_logger = Mock()
        mock_logger.level = logging.INFO

        with log_context(logger=mock_logger, level=logging.DEBUG):
            # DEBUG level within the context
            assert mock_logger.setLevel.call_args_list[-1][0][0] == logging.DEBUG

        # Returns to original level after exiting context
        assert mock_logger.setLevel.call_args_list[-1][0][0] == logging.INFO

    def test_restores_original_level_on_exception(self) -> None:
        mock_logger = Mock()
        mock_logger.level = logging.WARNING

        with pytest.raises(ValueError):
            with log_context(logger=mock_logger, level=logging.ERROR):
                # ERROR level within the context
                assert mock_logger.setLevel.call_args_list[-1][0][0] == logging.ERROR
                raise ValueError("Test error")

        # Returns to original level even if exception occurs
        assert mock_logger.setLevel.call_args_list[-1][0][0] == logging.WARNING

    def test_works_with_string_logger_name(self) -> None:
        # Test with actual logger
        logger_name = "test_context_logger"
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)

        with log_context(logger=logger_name, level=logging.DEBUG):
            # DEBUG level within the context
            assert logger.level == logging.DEBUG

        # Returns to original level after exiting context
        assert logger.level == logging.INFO

    def test_accepts_logger_instance(self) -> None:
        logger = logging.getLogger("test_logger_instance")
        logger.setLevel(logging.ERROR)

        with log_context(logger=logger, level=logging.INFO):
            assert logger.level == logging.INFO

        assert logger.level == logging.ERROR

    def test_nested_contexts(self) -> None:
        # Test nesting with actual logger
        logger = logging.getLogger("test_nested_logger")
        logger.setLevel(logging.WARNING)

        with log_context(logger=logger, level=logging.INFO):
            # First context
            assert logger.level == logging.INFO
            original_in_first_context = logger.level

            with log_context(logger=logger, level=logging.DEBUG):
                # Nested context
                assert logger.level == logging.DEBUG

            # After exiting inner context, returns to the "original level" recorded by inner context
            # (which will be INFO)
            assert logger.level == original_in_first_context

        # After exiting outer context, returns to original WARNING
        assert logger.level == logging.WARNING
