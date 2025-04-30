# __main__.py

import logging
from time import sleep

from rich import print
from rich.panel import Panel

from richlog import DateFormat, LogFormat, get_rich_logger


def display_intro():
    print(
        Panel(
            "[bold blue]Rich Log Example[/bold blue]\nDemonstrating different logging formats and levels.",
            title="Introduction",
        )
    )


def log_examples():
    # Create loggers for various scenarios
    loggers = [
        get_rich_logger(
            name="simple_logger",
            level=logging.DEBUG,
            log_format=LogFormat.SIMPLE,
            date_format=DateFormat.DEFAULT,
        ),
        get_rich_logger(
            name="verbose_logger",
            level=logging.DEBUG,
            log_format=LogFormat.VERBOSE,
            date_format=DateFormat.ISO8601,
        ),
        get_rich_logger(
            name="detailed_logger",
            level=logging.DEBUG,
            log_format=LogFormat.DETAILED,
            date_format=DateFormat.US,
        ),
    ]

    # Example messages with different levels
    messages = [
        ("This is a debug message for detailed inspection.", logging.DEBUG),
        ("Here's an info message, letting you know what's happening.", logging.INFO),
        ("Warning! There's something fishy going on.", logging.WARNING),
        ("Error! Something went wrong!", logging.ERROR),
        ("Critical error! Immediate attention needed!", logging.CRITICAL),
    ]

    for logger in loggers:
        for message, level in messages:
            logger.log(level, message)
            sleep(0.1)


def main():
    display_intro()
    log_examples()
    print(
        Panel(
            "[bold green]Finished logging examples. Goodbye![/bold green]",
            title="Conclusion",
        )
    )


if __name__ == "__main__":
    main()
