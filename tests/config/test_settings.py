import logging
import os
from pathlib import Path
from unittest.mock import patch

from richlog.config.settings import Settings, load_settings


class TestSettings:
    def test_default_settings(self) -> None:
        settings = Settings()
        assert settings.level == "INFO"
        assert settings.format == "DEFAULT"
        assert settings.date_format == "DEFAULT"
        assert settings.rich_tracebacks is True
        assert settings.traceback_suppress == []

    def test_custom_settings(self) -> None:
        settings = Settings(
            level="DEBUG",
            format="VERBOSE",
            date_format="ISO8601",
            rich_tracebacks=False,
            traceback_suppress=["module1", "module2"],
        )
        assert settings.level == "DEBUG"
        assert settings.format == "VERBOSE"
        assert settings.date_format == "ISO8601"
        assert settings.rich_tracebacks is False
        assert settings.traceback_suppress == ["module1", "module2"]

    def test_get_log_level(self) -> None:
        settings = Settings(level="DEBUG")
        assert settings.get_log_level() == logging.DEBUG

        settings = Settings(level="INFO")
        assert settings.get_log_level() == logging.INFO

        settings = Settings(level="WARNING")
        assert settings.get_log_level() == logging.WARNING

        settings = Settings(level="ERROR")
        assert settings.get_log_level() == logging.ERROR

        settings = Settings(level="CRITICAL")
        assert settings.get_log_level() == logging.CRITICAL

    def test_get_log_level_invalid(self) -> None:
        settings = Settings(level="INVALID")
        # デフォルトのINFOレベルが返される
        assert settings.get_log_level() == logging.INFO


class TestLoadSettings:
    def test_load_settings_from_env(self) -> None:
        with patch.dict(os.environ, {
            "RICHLOG_LEVEL": "DEBUG",
            "RICHLOG_FORMAT": "DETAILED",
            "RICHLOG_DATE_FORMAT": "US",
            "RICHLOG_RICH_TRACEBACKS": "false",
            "RICHLOG_TRACEBACK_SUPPRESS": "module1,module2",
        }):
            settings = load_settings()
            assert settings.level == "DEBUG"
            assert settings.format == "DETAILED"
            assert settings.date_format == "US"
            assert settings.rich_tracebacks is False
            assert settings.traceback_suppress == ["module1", "module2"]

    def test_load_settings_from_file(self, tmp_path: Path) -> None:
        # 設定ファイルを作成
        config_file = tmp_path / ".richlogrc"
        config_file.write_text("""
[richlog]
level = ERROR
format = SIMPLE
date_format = EU
rich_tracebacks = true
traceback_suppress = package1,package2
""")

        settings = load_settings(config_path=config_file)
        assert settings.level == "ERROR"
        assert settings.format == "SIMPLE"
        assert settings.date_format == "EU"
        assert settings.rich_tracebacks is True
        assert settings.traceback_suppress == ["package1", "package2"]

    def test_load_settings_env_overrides_file(self, tmp_path: Path) -> None:
        # 設定ファイルを作成
        config_file = tmp_path / ".richlogrc"
        config_file.write_text("""
[richlog]
level = ERROR
format = SIMPLE
""")

        # 環境変数がファイル設定を上書きする
        with patch.dict(os.environ, {
            "RICHLOG_LEVEL": "DEBUG",
        }):
            settings = load_settings(config_path=config_file)
            assert settings.level == "DEBUG"  # 環境変数の値
            assert settings.format == "SIMPLE"  # ファイルの値

    def test_load_settings_no_config(self) -> None:
        # 環境変数をクリア
        with patch.dict(os.environ, clear=True):
            settings = load_settings()
            # デフォルト値が使用される
            assert settings.level == "INFO"
            assert settings.format == "DEFAULT"

    def test_load_settings_toml_format(self, tmp_path: Path) -> None:
        # TOMLファイルでの設定
        config_file = tmp_path / "richlog.toml"
        config_file.write_text("""
[richlog]
level = "WARNING"
format = "VERBOSE"
date_format = "ISO8601"
rich_tracebacks = false
traceback_suppress = ["foo", "bar"]
""")

        settings = load_settings(config_path=config_file)
        assert settings.level == "WARNING"
        assert settings.format == "VERBOSE"
        assert settings.date_format == "ISO8601"
        assert settings.rich_tracebacks is False
        assert settings.traceback_suppress == ["foo", "bar"]
