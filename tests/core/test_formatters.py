import pytest

from richlog.core.formatters import DateFormat, LogFormat


class TestLogFormat:
    def test_default_format(self) -> None:
        assert LogFormat.DEFAULT == "%(message)s"

    def test_verbose_format(self) -> None:
        assert LogFormat.VERBOSE == "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    def test_simple_format(self) -> None:
        assert LogFormat.SIMPLE == "%(levelname)s: %(message)s"

    def test_detailed_format(self) -> None:
        expected = (
            "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
        )
        assert LogFormat.DETAILED == expected

    def test_nothing_format(self) -> None:
        assert LogFormat.NOTHING == ""

    def test_format_is_immutable(self) -> None:
        # LogFormatがfrozen dataclassであることを確認
        log_format = LogFormat()
        with pytest.raises(AttributeError):
            log_format.DEFAULT = "new format"  # type: ignore


class TestDateFormat:
    def test_default_format(self) -> None:
        assert DateFormat.DEFAULT == "%Y-%m-%d %H:%M:%S"

    def test_iso8601_format(self) -> None:
        assert DateFormat.ISO8601 == "%Y-%m-%dT%H:%M:%S"

    def test_us_format(self) -> None:
        assert DateFormat.US == "%m/%d/%Y %I:%M:%S %p"

    def test_eu_format(self) -> None:
        assert DateFormat.EU == "%d/%m/%Y %H:%M:%S"

    def test_nothing_format(self) -> None:
        assert DateFormat.NOTHING == ""

    def test_format_is_immutable(self) -> None:
        # DateFormatがfrozen dataclassであることを確認
        date_format = DateFormat()
        with pytest.raises(AttributeError):
            date_format.DEFAULT = "new format"  # type: ignore
