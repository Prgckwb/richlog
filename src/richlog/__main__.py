#!/usr/bin/env python3
"""
RichLog Demo - Interactive demonstration of all RichLog features.

This module provides a comprehensive showcase of the RichLog library's capabilities,
including various log formats, handlers, decorators, and configuration options.
"""

import argparse
import json
import logging
import os
import tempfile
import time
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt
from rich.table import Table

from richlog import (
    CRITICAL,
    DEBUG,
    ERROR,
    INFO,
    WARNING,
    AsyncHandler,
    BufferedHandler,
    DateFormat,
    JSONHandler,
    LogFormat,
    configure_from_dict,
    get_rich_logger,
    load_settings,
    log_context,
    log_errors,
    log_execution_time,
    setup_file_logger,
    setup_json_logger,
    setup_logger_with_preset,
)

console = Console()


def display_banner():
    """Display the RichLog demo banner."""
    banner = """[bold blue]╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║                    [bold yellow]RichLog Feature Demo[/bold yellow]                      ║
║                                                               ║
║  A comprehensive demonstration of RichLog's logging features  ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝[/bold blue]"""
    console.print(banner)
    console.print()


def demo_basic_formats():
    """Demonstrate all available log formats and date formats."""
    console.print(Panel("[bold cyan]Basic Log Formats Demo[/bold cyan]", title="Demo 1"))

    # Show all log formats
    console.print("\n[bold]Available Log Formats:[/bold]")
    formats_table = Table(show_header=True, header_style="bold magenta")
    formats_table.add_column("Format", style="cyan")
    formats_table.add_column("Example Output")

    for format_name in ["DEFAULT", "SIMPLE", "VERBOSE", "DETAILED", "NOTHING"]:
        log_format = getattr(LogFormat, format_name)
        logger = get_rich_logger(f"demo_{format_name.lower()}", level=INFO, log_format=log_format)
        formats_table.add_row(format_name, f"[dim]{log_format}[/dim]")

    console.print(formats_table)

    # Show all date formats
    console.print("\n[bold]Available Date Formats:[/bold]")
    date_table = Table(show_header=True, header_style="bold magenta")
    date_table.add_column("Format", style="cyan")
    date_table.add_column("Pattern")
    date_table.add_column("Example")

    from datetime import datetime

    now = datetime.now()

    for format_name in ["DEFAULT", "ISO8601", "US", "EU", "NOTHING"]:
        date_format = getattr(DateFormat, format_name)
        if date_format:
            example = now.strftime(date_format)
        else:
            example = "(no timestamp)"
        date_table.add_row(format_name, f"[dim]{date_format}[/dim]", example)

    console.print(date_table)

    # Live demonstration
    console.print("\n[bold]Live Examples:[/bold]")
    for log_format in [LogFormat.DEFAULT, LogFormat.SIMPLE, LogFormat.VERBOSE, LogFormat.DETAILED]:
        logger = get_rich_logger(
            f"example_{log_format.name.lower()}",
            level=INFO,
            log_format=log_format,
            date_format=DateFormat.ISO8601,
        )
        logger.info(f"Demo with {log_format.name} format")
        time.sleep(0.1)


def demo_log_levels():
    """Demonstrate all logging levels with colorful output."""
    console.print(Panel("[bold cyan]Log Levels Demo[/bold cyan]", title="Demo 2"))

    logger = get_rich_logger("levels_demo", level=DEBUG, log_format=LogFormat.SIMPLE)

    levels = [
        (DEBUG, "Debug information for developers", "🐛"),
        (INFO, "Informational message", "i"),
        (WARNING, "Warning: something needs attention", "⚠️"),
        (ERROR, "Error: something went wrong", "❌"),
        (CRITICAL, "Critical: system failure imminent", "🚨"),
    ]

    console.print("\n[bold]All Log Levels:[/bold]")
    for level, message, emoji in levels:
        logger.log(level, f"{emoji} {message}")
        time.sleep(0.2)


def demo_presets():
    """Demonstrate preset configurations."""
    console.print(Panel("[bold cyan]Preset Configurations Demo[/bold cyan]", title="Demo 3"))

    presets = ["development", "production", "testing"]

    console.print("\n[bold]Available Presets:[/bold]")
    for preset in presets:
        console.print(f"\n[yellow]Preset: {preset}[/yellow]")
        logger = setup_logger_with_preset(f"preset_{preset}", preset=preset)  # type: ignore

        # Show configuration
        if preset == "development":
            console.print("  • Level: DEBUG")
            console.print("  • Format: DETAILED")
            console.print("  • Rich tracebacks: Enabled")
        elif preset == "production":
            console.print("  • Level: INFO")
            console.print("  • Format: VERBOSE")
            console.print("  • Rich tracebacks: Disabled")
        else:  # testing
            console.print("  • Level: DEBUG")
            console.print("  • Format: SIMPLE")
            console.print("  • Rich tracebacks: Enabled")

        logger.info(f"Message from {preset} preset")
        if preset == "development":
            logger.debug("Debug info only shown in development")


def demo_handlers():
    """Demonstrate different handlers."""
    console.print(Panel("[bold cyan]Advanced Handlers Demo[/bold cyan]", title="Demo 4"))

    with tempfile.TemporaryDirectory() as tmpdir:
        # File handler with rotation
        console.print("\n[bold]1. File Handler with Rotation:[/bold]")
        file_logger = setup_file_logger(
            "file_demo",
            filename=str(Path(tmpdir) / "demo.log"),
            max_bytes=1000,  # Small size for demo
            backup_count=3,
            level=DEBUG,
        )

        console.print("  Writing multiple messages to trigger rotation...")
        with Progress(
            SpinnerColumn(), TextColumn("[progress.description]{task.description}")
        ) as progress:
            task = progress.add_task("Writing logs...", total=50)
            for i in range(50):
                file_logger.info(f"Message {i + 1}: " + "x" * 50)
                progress.update(task, advance=1)
                time.sleep(0.01)

        log_files = list(Path(tmpdir).glob("demo.log*"))
        console.print(f"  Created {len(log_files)} log files (with rotation)")

        # JSON handler
        console.print("\n[bold]2. JSON Handler:[/bold]")
        json_logger = setup_json_logger("json_demo", include_console=False)

        # Capture JSON output
        json_output = []

        class CaptureJSONHandler(JSONHandler):
            def emit(self, record):
                json_output.append(json.loads(self.format(record)))

        json_logger.handlers.clear()
        capture_handler = CaptureJSONHandler()
        json_logger.addHandler(capture_handler)

        json_logger.info("User logged in", extra={"user_id": 12345, "ip": "192.168.1.100"})
        json_logger.warning("API rate limit approaching", extra={"remaining": 10, "limit": 100})

        console.print("  JSON output examples:")
        for entry in json_output:
            console.print(f"  {json.dumps(entry, indent=2)}")

        # Async handler
        console.print("\n[bold]3. Async Handler (Non-blocking):[/bold]")
        base_handler = logging.StreamHandler()
        async_handler = AsyncHandler(base_handler)
        async_logger = logging.getLogger("async_demo")
        async_logger.setLevel(DEBUG)
        async_logger.addHandler(async_handler)

        console.print("  Sending messages asynchronously...")
        start = time.time()
        for i in range(10):
            async_logger.info(f"Async message {i + 1}")
        elapsed = time.time() - start
        console.print(f"  Completed in {elapsed:.4f} seconds (non-blocking)")

        # Buffered handler
        console.print("\n[bold]4. Buffered Handler:[/bold]")
        buffered_json = BufferedHandler(JSONHandler(), buffer_size=5)
        buffer_logger = logging.getLogger("buffer_demo")
        buffer_logger.setLevel(DEBUG)
        buffer_logger.addHandler(buffered_json)

        console.print("  Buffering messages (buffer size: 5)...")
        for i in range(7):
            buffer_logger.info(f"Buffered message {i + 1}")
            console.print(f"    Added message {i + 1}")
            if i == 4:
                console.print("    [yellow]→ Buffer full, flushing...[/yellow]")
            time.sleep(0.1)

        buffered_json.flush()
        console.print("    [green]→ Final flush completed[/green]")


def demo_decorators():
    """Demonstrate logging decorators."""
    console.print(Panel("[bold cyan]Decorators Demo[/bold cyan]", title="Demo 5"))

    logger = get_rich_logger("decorator_demo", level=DEBUG, log_format=LogFormat.DETAILED)

    # Execution time decorator
    console.print("\n[bold]1. Execution Time Decorator:[/bold]")

    @log_execution_time(logger, level=INFO)
    def slow_function(duration: float) -> str:
        """Simulate a slow operation."""
        time.sleep(duration)
        return f"Completed after {duration} seconds"

    console.print("  Running slow function...")
    result = slow_function(0.5)
    console.print(f"  Result: {result}")

    # Error logging decorator
    console.print("\n[bold]2. Error Logging Decorator:[/bold]")

    @log_errors(logger, level=ERROR, reraise=False)
    def risky_function(should_fail: bool) -> str:
        """Function that might fail."""
        if should_fail:
            raise ValueError("Intentional error for demo")
        return "Success!"

    console.print("  Testing successful execution:")
    result = risky_function(False)
    console.print(f"  Result: {result}")

    console.print("\n  Testing error handling:")
    result = risky_function(True)
    console.print(f"  Result: {result} (error was logged but not raised)")

    # Combined decorators
    console.print("\n[bold]3. Combined Decorators:[/bold]")

    @log_errors(logger, reraise=False)
    @log_execution_time(logger)
    def complex_function(x: int) -> int:
        """Function with both decorators."""
        time.sleep(0.1)
        if x < 0:
            raise ValueError("Negative input not allowed")
        return x * 2

    console.print("  Testing with valid input:")
    result = complex_function(5)
    console.print(f"  Result: {result}")

    console.print("\n  Testing with invalid input:")
    result = complex_function(-5)
    console.print(f"  Result: {result}")


def demo_context_manager():
    """Demonstrate the log level context manager."""
    console.print(Panel("[bold cyan]Context Manager Demo[/bold cyan]", title="Demo 6"))

    logger = get_rich_logger("context_demo", level=INFO, log_format=LogFormat.SIMPLE)

    console.print("\n[bold]Temporary Log Level Changes:[/bold]")

    console.print("\nNormal logging (INFO level):")
    logger.info("This INFO message is visible")
    logger.debug("This DEBUG message is NOT visible")

    console.print("\nInside debug context:")
    with log_context(logger, DEBUG):
        logger.info("This INFO message is still visible")
        logger.debug("This DEBUG message is NOW visible!")

        console.print("\n  Nested context (WARNING level):")
        with log_context(logger, WARNING):
            logger.warning("This WARNING is visible")
            logger.info("This INFO is NOT visible in nested context")
            logger.debug("This DEBUG is NOT visible in nested context")

    console.print("\nBack to normal (INFO level):")
    logger.info("INFO is visible again")
    logger.debug("DEBUG is NOT visible again")


def demo_configuration():
    """Demonstrate configuration options."""
    console.print(Panel("[bold cyan]Configuration Demo[/bold cyan]", title="Demo 7"))

    with tempfile.TemporaryDirectory() as tmpdir:
        # Environment variables
        console.print("\n[bold]1. Environment Variables:[/bold]")
        os.environ["RICHLOG_LEVEL"] = "WARNING"
        os.environ["RICHLOG_FORMAT"] = "DETAILED"
        os.environ["RICHLOG_DATE_FORMAT"] = "US"
        os.environ["RICHLOG_RICH_TRACEBACKS"] = "false"

        settings = load_settings()
        console.print("  Loaded from environment:")
        console.print(f"    Level: {settings.level}")
        console.print(f"    Format: {settings.format}")
        console.print(f"    Date Format: {settings.date_format}")
        console.print(f"    Rich Tracebacks: {settings.rich_tracebacks}")

        env_logger = settings.create_logger("env_config")
        env_logger.warning("Message using environment config")

        # Clean up env vars
        for key in [
            "RICHLOG_LEVEL",
            "RICHLOG_FORMAT",
            "RICHLOG_DATE_FORMAT",
            "RICHLOG_RICH_TRACEBACKS",
        ]:
            os.environ.pop(key, None)

        # TOML configuration
        console.print("\n[bold]2. TOML Configuration:[/bold]")
        toml_path = Path(tmpdir) / "richlog.toml"
        toml_path.write_text("""
[richlog]
level = "DEBUG"
format = "VERBOSE"
date_format = "EU"
rich_tracebacks = true
traceback_suppress = ["urllib3", "requests"]
""")

        toml_settings = load_settings(toml_path)
        console.print("  Loaded from TOML:")
        console.print(f"    Level: {toml_settings.level}")
        console.print(f"    Format: {toml_settings.format}")
        console.print(f"    Date Format: {toml_settings.date_format}")
        console.print(f"    Suppress: {toml_settings.traceback_suppress}")

        toml_logger = toml_settings.create_logger("toml_config")
        toml_logger.debug("Message using TOML config")

        # Dictionary configuration
        console.print("\n[bold]3. Dictionary Configuration:[/bold]")
        config_dict = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {"custom": {"format": "%(levelname)-8s | %(name)-15s | %(message)s"}},
            "handlers": {
                "console": {"class": "richlog.RichHandler", "level": "DEBUG", "formatter": "custom"}
            },
            "loggers": {
                "dict_config": {"level": "DEBUG", "handlers": ["console"], "propagate": False}
            },
        }

        configure_from_dict(config_dict)
        dict_logger = logging.getLogger("dict_config")
        dict_logger.info("Message using dictionary config")


def demo_custom_formats():
    """Demonstrate custom format strings."""
    console.print(Panel("[bold cyan]Custom Formats Demo[/bold cyan]", title="Demo 8"))

    console.print("\n[bold]Custom Log Format:[/bold]")
    custom_format = "🔸 %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s"
    logger = get_rich_logger(
        "custom_demo", level=DEBUG, log_format=custom_format, date_format="%H:%M:%S"
    )

    def example_function():
        logger.debug("Debug from function")
        logger.info("Info from function")
        logger.warning("Warning from function")

    example_function()

    console.print("\n[bold]Custom Date Format:[/bold]")
    fancy_date = "%A, %B %d, %Y at %I:%M %p"
    fancy_logger = get_rich_logger(
        "fancy_date", level=INFO, log_format=LogFormat.VERBOSE, date_format=fancy_date
    )
    fancy_logger.info("Message with fancy date format")


def demo_exception_handling():
    """Demonstrate exception handling with rich tracebacks."""
    console.print(Panel("[bold cyan]Exception Handling Demo[/bold cyan]", title="Demo 9"))

    logger = get_rich_logger(
        "exception_demo",
        level=DEBUG,
        log_format=LogFormat.DETAILED,
        rich_tracebacks=True,
        traceback_suppress=["typing", "functools"],
    )

    console.print("\n[bold]Rich Traceback Example:[/bold]")

    def inner_function():
        raise ValueError("This is an intentional error for demonstration")

    def middle_function():
        inner_function()

    def outer_function():
        middle_function()

    try:
        outer_function()
    except Exception:
        logger.exception("Caught an exception with rich traceback:")


def interactive_menu():
    """Interactive menu for selecting demos."""
    demos = [
        ("Basic Formats", demo_basic_formats),
        ("Log Levels", demo_log_levels),
        ("Preset Configurations", demo_presets),
        ("Advanced Handlers", demo_handlers),
        ("Decorators", demo_decorators),
        ("Context Manager", demo_context_manager),
        ("Configuration Options", demo_configuration),
        ("Custom Formats", demo_custom_formats),
        ("Exception Handling", demo_exception_handling),
    ]

    while True:
        console.print("\n[bold cyan]Select a demo:[/bold cyan]")
        for i, (name, _) in enumerate(demos, 1):
            console.print(f"  {i}. {name}")
        console.print("  0. Exit")

        choice = Prompt.ask("\nEnter your choice", choices=[str(i) for i in range(len(demos) + 1)])

        if choice == "0":
            break

        idx = int(choice) - 1
        console.clear()
        display_banner()
        demos[idx][1]()

        if not Confirm.ask("\nWould you like to see another demo?"):
            break


def run_all_demos():
    """Run all demos in sequence."""
    demos = [
        demo_basic_formats,
        demo_log_levels,
        demo_presets,
        demo_handlers,
        demo_decorators,
        demo_context_manager,
        demo_configuration,
        demo_custom_formats,
        demo_exception_handling,
    ]

    for i, demo in enumerate(demos, 1):
        demo()
        if i < len(demos):
            console.print("\n" + "─" * 60 + "\n")
            time.sleep(0.5)


def main():
    """Main entry point for the RichLog demo."""
    parser = argparse.ArgumentParser(
        description="RichLog Feature Demo - Interactive demonstration of all RichLog features",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m richlog              # Interactive menu
  python -m richlog --all        # Run all demos
  python -m richlog --demo 1     # Run specific demo
  python -m richlog --list       # List all demos
        """,
    )

    parser.add_argument("--all", "-a", action="store_true", help="Run all demos in sequence")

    parser.add_argument("--demo", "-d", type=int, metavar="N", help="Run specific demo by number")

    parser.add_argument("--list", "-l", action="store_true", help="List all available demos")

    parser.add_argument("--version", "-v", action="store_true", help="Show RichLog version")

    args = parser.parse_args()

    if args.version:
        from richlog import __version__

        console.print(f"[bold]RichLog version:[/bold] {__version__}")
        return

    if args.list:
        console.print("[bold]Available demos:[/bold]")
        demos = [
            "Basic Formats",
            "Log Levels",
            "Preset Configurations",
            "Advanced Handlers",
            "Decorators",
            "Context Manager",
            "Configuration Options",
            "Custom Formats",
            "Exception Handling",
        ]
        for i, name in enumerate(demos, 1):
            console.print(f"  {i}. {name}")
        return

    display_banner()

    if args.all:
        run_all_demos()
        console.print("\n[bold green]All demos completed![/bold green]")
    elif args.demo:
        demos = [
            demo_basic_formats,
            demo_log_levels,
            demo_presets,
            demo_handlers,
            demo_decorators,
            demo_context_manager,
            demo_configuration,
            demo_custom_formats,
            demo_exception_handling,
        ]
        if 1 <= args.demo <= len(demos):
            demos[args.demo - 1]()
        else:
            console.print(
                f"[bold red]Error:[/bold red] Demo {args.demo} does not exist. "
                "Use --list to see available demos."
            )
    else:
        interactive_menu()

    console.print("\n[bold blue]Thank you for exploring RichLog![/bold blue] 🎉")


if __name__ == "__main__":
    main()
