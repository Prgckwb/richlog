from richlog.core.formatters import DateFormat, LogFormat


class TestLogFormat:
    def test_default_format(self) -> None:
        assert LogFormat.DEFAULT == "%(message)s"
        assert LogFormat.DEFAULT.value == "%(message)s"

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

    def test_enum_behavior(self) -> None:
        # Verify enum behavior
        assert LogFormat.DEFAULT.name == "DEFAULT"
        assert LogFormat.DEFAULT.value == "%(message)s"
        assert isinstance(LogFormat.DEFAULT, str)

    def test_from_string(self) -> None:
        # Case insensitive
        assert LogFormat.from_string("default") == LogFormat.DEFAULT
        assert LogFormat.from_string("DEFAULT") == LogFormat.DEFAULT
        assert LogFormat.from_string("Simple") == LogFormat.SIMPLE

    def test_from_string_custom_format(self) -> None:
        # Custom format string
        custom = "%(levelname)s | %(message)s"
        result = LogFormat.from_string(custom)
        assert result == custom
        assert isinstance(result, str)

    def test_all_formats_available(self) -> None:
        # Verify all formats are available
        formats = [
            LogFormat.DEFAULT,
            LogFormat.SIMPLE,
            LogFormat.VERBOSE,
            LogFormat.DETAILED,
            LogFormat.NOTHING,
        ]
        assert len(formats) == 5
        assert all(isinstance(fmt, LogFormat) for fmt in formats)


class TestDateFormat:
    def test_default_format(self) -> None:
        assert DateFormat.DEFAULT == "%Y-%m-%d %H:%M:%S"
        assert DateFormat.DEFAULT.value == "%Y-%m-%d %H:%M:%S"

    def test_iso8601_format(self) -> None:
        assert DateFormat.ISO8601 == "%Y-%m-%dT%H:%M:%S"

    def test_us_format(self) -> None:
        assert DateFormat.US == "%m/%d/%Y %I:%M:%S %p"

    def test_eu_format(self) -> None:
        assert DateFormat.EU == "%d/%m/%Y %H:%M:%S"

    def test_nothing_format(self) -> None:
        assert DateFormat.NOTHING == ""

    def test_enum_behavior(self) -> None:
        # Verify enum behavior
        assert DateFormat.ISO8601.name == "ISO8601"
        assert DateFormat.ISO8601.value == "%Y-%m-%dT%H:%M:%S"
        assert isinstance(DateFormat.ISO8601, str)

    def test_from_string(self) -> None:
        # Case insensitive
        assert DateFormat.from_string("iso8601") == DateFormat.ISO8601
        assert DateFormat.from_string("ISO8601") == DateFormat.ISO8601
        assert DateFormat.from_string("us") == DateFormat.US

    def test_from_string_custom_format(self) -> None:
        # Custom date format
        custom = "%Y-%m-%d %H:%M"
        result = DateFormat.from_string(custom)
        assert result == custom
        assert isinstance(result, str)

    def test_all_formats_available(self) -> None:
        # Verify all formats are available
        formats = [
            DateFormat.DEFAULT,
            DateFormat.ISO8601,
            DateFormat.US,
            DateFormat.EU,
            DateFormat.NOTHING,
        ]
        assert len(formats) == 5
        assert all(isinstance(fmt, DateFormat) for fmt in formats)
