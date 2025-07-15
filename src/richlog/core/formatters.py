from dataclasses import dataclass


@dataclass(frozen=True)
class LogFormat:
    DEFAULT: str = "%(message)s"
    VERBOSE: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    SIMPLE: str = "%(levelname)s: %(message)s"
    DETAILED: str = (
        "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
    )
    NOTHING: str = ""


@dataclass(frozen=True)
class DateFormat:
    DEFAULT: str = "%Y-%m-%d %H:%M:%S"
    ISO8601: str = "%Y-%m-%dT%H:%M:%S"
    US: str = "%m/%d/%Y %I:%M:%S %p"
    EU: str = "%d/%m/%Y %H:%M:%S"
    NOTHING: str = ""
