from richlog.config.defaults import (
    DEFAULT_DATE_FORMAT,
    DEFAULT_LEVEL,
    DEFAULT_LOG_FORMAT,
    DEFAULT_RICH_TRACEBACKS,
    DEFAULT_TRACEBACK_SUPPRESS,
)


class TestDefaults:
    def test_default_level(self) -> None:
        assert DEFAULT_LEVEL == "INFO"

    def test_default_log_format(self) -> None:
        assert DEFAULT_LOG_FORMAT == "DEFAULT"

    def test_default_date_format(self) -> None:
        assert DEFAULT_DATE_FORMAT == "DEFAULT"

    def test_default_rich_tracebacks(self) -> None:
        assert DEFAULT_RICH_TRACEBACKS is True

    def test_default_traceback_suppress(self) -> None:
        assert DEFAULT_TRACEBACK_SUPPRESS == []
        # Verify list is mutable
        assert isinstance(DEFAULT_TRACEBACK_SUPPRESS, list)
