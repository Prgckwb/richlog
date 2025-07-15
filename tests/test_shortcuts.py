"""Tests for shortcut functions"""

import logging
from pathlib import Path
from unittest.mock import MagicMock, patch

from richlog.shortcuts import (
    configure_from_dict,
    setup_file_logger,
    setup_json_logger,
    setup_logger_with_preset,
)


class TestSetupLoggerWithPreset:
    """Tests for setup_logger_with_preset function"""

    def test_default_preset(self) -> None:
        """Test with default development preset"""
        logger = setup_logger_with_preset("test_logger")
        assert logger.name == "test_logger"
        assert logger.level == logging.DEBUG
        assert len(logger.handlers) == 1

    def test_production_preset(self) -> None:
        """Test with production preset"""
        logger = setup_logger_with_preset("prod_logger", preset="production")
        assert logger.name == "prod_logger"
        assert logger.level == logging.INFO
        assert len(logger.handlers) == 1

    def test_testing_preset(self) -> None:
        """Test with testing preset"""
        logger = setup_logger_with_preset("test_logger", preset="testing")
        assert logger.name == "test_logger"
        assert logger.level == logging.DEBUG
        assert len(logger.handlers) == 1

    def test_with_overrides(self) -> None:
        """Test preset with overrides"""
        logger = setup_logger_with_preset(
            "override_logger", preset="development", level=logging.WARNING
        )
        assert logger.name == "override_logger"
        assert logger.level == logging.WARNING  # Override applied

    @patch("richlog.shortcuts.load_settings")
    def test_with_config_file(self, mock_load_settings: MagicMock) -> None:
        """Test loading from config file"""
        mock_settings = MagicMock()
        mock_settings.create_logger.return_value = logging.getLogger("config_logger")
        mock_load_settings.return_value = mock_settings

        config_path = Path("test_config.yaml")
        setup_logger_with_preset("config_logger", config_file=config_path)

        mock_load_settings.assert_called_once_with(config_path)
        mock_settings.create_logger.assert_called_once_with("config_logger")


class TestSetupFileLogger:
    """Tests for setup_file_logger function"""

    def test_creates_file_logger(self, tmp_path: Path) -> None:
        """Test that file logger is created correctly"""
        log_file = tmp_path / "test.log"
        logger = setup_file_logger(
            "file_logger",
            str(log_file),
            max_bytes=1000,
            backup_count=3,
            level=logging.DEBUG,
        )

        assert logger.name == "file_logger"
        assert logger.level == logging.DEBUG
        assert len(logger.handlers) == 2  # Rich handler + file handler

        # Test logging
        logger.info("Test message")
        assert log_file.exists()
        assert "Test message" in log_file.read_text()

    def test_default_parameters(self, tmp_path: Path) -> None:
        """Test with default parameters"""
        log_file = tmp_path / "app.log"
        logger = setup_file_logger(filename=str(log_file))

        assert logger.name == "app"
        assert logger.level == logging.INFO
        assert len(logger.handlers) == 2


class TestSetupJsonLogger:
    """Tests for setup_json_logger function"""

    def test_with_console(self) -> None:
        """Test JSON logger with console output"""
        logger = setup_json_logger("json_logger", include_console=True)

        assert logger.name == "json_logger"
        assert logger.level == logging.INFO
        assert len(logger.handlers) == 2  # Rich handler + JSON handler

    def test_without_console(self) -> None:
        """Test JSON logger without console output"""
        logger = setup_json_logger("json_only", include_console=False)

        assert logger.name == "json_only"
        assert logger.level == logging.INFO
        assert len(logger.handlers) == 1  # JSON handler only

    @patch("richlog.shortcuts.BufferedHandler")
    @patch("richlog.shortcuts.JSONHandler")
    def test_with_buffering(
        self, mock_json_handler: MagicMock, mock_buffered_handler: MagicMock
    ) -> None:
        """Test JSON logger with buffering"""
        setup_json_logger("buffered_logger", buffered=True, buffer_size=500)

        mock_json_handler.assert_called_once()
        mock_buffered_handler.assert_called_once_with(
            mock_json_handler.return_value, buffer_size=500
        )


class TestConfigureFromDict:
    """Tests for configure_from_dict function"""

    @patch("logging.config.dictConfig")
    def test_basic_config(self, mock_dict_config: MagicMock) -> None:
        """Test basic configuration"""
        config = {
            "version": 1,
            "disable_existing_loggers": False,
            "loggers": {
                "myapp": {
                    "level": "DEBUG",
                    "handlers": ["console"],
                }
            },
        }

        configure_from_dict(config)
        mock_dict_config.assert_called_once_with(config)

    @patch("logging.config.dictConfig")
    def test_richlog_handler_mapping(self, mock_dict_config: MagicMock) -> None:
        """Test that richlog.RichHandler is mapped correctly"""
        config = {
            "version": 1,
            "handlers": {
                "console": {
                    "class": "richlog.RichHandler",
                    "level": "DEBUG",
                }
            },
        }

        configure_from_dict(config)

        # Check that the handler class was remapped
        called_config = mock_dict_config.call_args[0][0]
        assert called_config["handlers"]["console"]["class"] == "rich.logging.RichHandler"
