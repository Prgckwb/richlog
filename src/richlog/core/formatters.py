from enum import Enum


class LogFormat(str, Enum):
    """ログフォーマットの定義"""

    DEFAULT = "%(message)s"
    SIMPLE = "%(levelname)s: %(message)s"
    VERBOSE = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DETAILED = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
    NOTHING = ""

    @classmethod
    def from_string(cls, value: str) -> "LogFormat":
        """文字列からLogFormatを取得（大文字小文字を区別しない）"""
        try:
            return cls[value.upper()]
        except KeyError:
            # カスタムフォーマット文字列の場合はそのまま返す
            return cls(value)


class DateFormat(str, Enum):
    """日付フォーマットの定義"""

    DEFAULT = "%Y-%m-%d %H:%M:%S"
    ISO8601 = "%Y-%m-%dT%H:%M:%S"
    US = "%m/%d/%Y %I:%M:%S %p"
    EU = "%d/%m/%Y %H:%M:%S"
    NOTHING = ""

    @classmethod
    def from_string(cls, value: str) -> "DateFormat":
        """文字列からDateFormatを取得（大文字小文字を区別しない）"""
        try:
            return cls[value.upper()]
        except KeyError:
            # カスタムフォーマット文字列の場合はそのまま返す
            return cls(value)
