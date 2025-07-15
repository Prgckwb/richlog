import logging
import time
from unittest.mock import Mock

import pytest

from richlog.utils.decorators import log_errors, log_execution_time


class TestLogExecutionTime:
    def test_logs_execution_time(self) -> None:
        # Mock the logger
        mock_logger = Mock()

        @log_execution_time(logger=mock_logger)
        def slow_function() -> str:
            time.sleep(0.1)
            return "done"

        result = slow_function()

        assert result == "done"
        # Verify log method was called
        mock_logger.log.assert_called_once()
        call_args = mock_logger.log.call_args
        assert call_args[0][0] == logging.INFO  # Log level
        log_message = call_args[0][1]
        assert "slow_function" in log_message
        assert "took" in log_message
        assert "seconds" in log_message

    def test_logs_with_custom_level(self) -> None:
        mock_logger = Mock()

        @log_execution_time(logger=mock_logger, level=logging.DEBUG)
        def test_function() -> int:
            return 42

        result = test_function()

        assert result == 42
        # Verify log method was called with DEBUG level
        mock_logger.log.assert_called_once()
        assert mock_logger.log.call_args[0][0] == logging.DEBUG

    def test_preserves_function_metadata(self) -> None:
        mock_logger = Mock()

        @log_execution_time(logger=mock_logger)
        def documented_function() -> None:
            """This is a documented function."""
            pass

        assert documented_function.__name__ == "documented_function"
        assert documented_function.__doc__ == "This is a documented function."

    def test_works_with_arguments(self) -> None:
        mock_logger = Mock()

        @log_execution_time(logger=mock_logger)
        def add(a: int, b: int) -> int:
            return a + b

        result = add(2, 3)
        assert result == 5
        mock_logger.log.assert_called_once()


class TestLogErrors:
    def test_logs_exceptions(self) -> None:
        mock_logger = Mock()

        @log_errors(logger=mock_logger)
        def failing_function() -> None:
            raise ValueError("Test error")

        with pytest.raises(ValueError):
            failing_function()

        # Verify log method was called with ERROR level
        mock_logger.log.assert_called_once()
        log_args = mock_logger.log.call_args
        assert log_args[0][0] == logging.ERROR
        assert "Error in failing_function" in log_args[0][1]
        assert log_args[1]["exc_info"] is True

    def test_logs_with_custom_level(self) -> None:
        mock_logger = Mock()

        @log_errors(logger=mock_logger, level=logging.WARNING)
        def failing_function() -> None:
            raise RuntimeError("Test error")

        with pytest.raises(RuntimeError):
            failing_function()

        # Verify log method was called with WARNING level
        mock_logger.log.assert_called_once()
        assert mock_logger.log.call_args[0][0] == logging.WARNING

    def test_does_not_log_on_success(self) -> None:
        mock_logger = Mock()

        @log_errors(logger=mock_logger)
        def successful_function() -> str:
            return "success"

        result = successful_function()

        assert result == "success"
        # Verify no log was recorded
        mock_logger.log.assert_not_called()

    def test_reraises_exception(self) -> None:
        mock_logger = Mock()

        @log_errors(logger=mock_logger)
        def failing_function() -> None:
            raise TypeError("Original error")

        with pytest.raises(TypeError, match="Original error"):
            failing_function()

    def test_with_reraise_false(self) -> None:
        mock_logger = Mock()

        @log_errors(logger=mock_logger, reraise=False)
        def failing_function() -> None:
            raise ValueError("Suppressed error")

        # Exception is suppressed
        result = failing_function()
        assert result is None
        mock_logger.log.assert_called_once()

    def test_preserves_function_metadata(self) -> None:
        mock_logger = Mock()

        @log_errors(logger=mock_logger)
        def documented_function() -> None:
            """This is a documented function."""
            pass

        assert documented_function.__name__ == "documented_function"
        assert documented_function.__doc__ == "This is a documented function."
