from enum import Enum


class LogFormat(str, Enum):
    """ログフォーマットの定義"""

    DEFAULT = "%(message)s"
    SIMPLE = "%(levelname)s: %(message)s"
    VERBOSE = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DETAILED = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
    NOTHING = ""

    @classmethod
    def from_string(cls, value: str) -> str:
        """Get LogFormat from string (case insensitive) or return custom format"""
        try:
            return cls[value.upper()]
        except KeyError:
            # Return custom format string as-is
            return value


class DateFormat(str, Enum):
    """日付フォーマットの定義"""

    DEFAULT = "%Y-%m-%d %H:%M:%S"
    ISO8601 = "%Y-%m-%dT%H:%M:%S"
    US = "%m/%d/%Y %I:%M:%S %p"
    EU = "%d/%m/%Y %H:%M:%S"
    NOTHING = ""

    @classmethod
    def from_string(cls, value: str) -> str:
        """Get DateFormat from string (case insensitive) or return custom format"""
        try:
            return cls[value.upper()]
        except KeyError:
            # Return custom format string as-is
            return value
