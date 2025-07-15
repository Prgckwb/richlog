# RichLog

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
[![CI](https://github.com/prgckwb/richlog/actions/workflows/ci.yml/badge.svg)](https://github.com/prgckwb/richlog/actions/workflows/ci.yml)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

RichLog is a powerful Python logging library that enhances your logging experience with the rich capabilities of the `rich` library. It provides beautiful, customizable console output with advanced features for production-ready applications.

## Features

- 🎨 **Beautiful Console Output** - Colorful, formatted logs using the `rich` library
- 📝 **Multiple Log Formats** - Simple, verbose, detailed, and custom formats with type-safe Enums
- 📅 **Flexible Date Formatting** - ISO8601, US, EU, and custom date formats
- 🔧 **Advanced Handlers** - File rotation, JSON output, async logging, and buffered logging
- ⚙️ **Configuration Management** - Environment variables and config file support with validation
- 🎯 **Useful Decorators** - Log execution time and catch errors automatically
- 🔄 **Context Managers** - Temporarily change log levels within code blocks
- 🚀 **Production Ready** - Type hints, comprehensive tests, and CI/CD pipeline
- ⚡ **Easy Setup** - Quick start with presets and shortcuts

## Installation

Install RichLog directly from GitHub:

```bash
pip install git+https://github.com/prgckwb/richlog.git
```

Or using [uv](https://github.com/astral-sh/uv):

```bash
uv pip install git+https://github.com/prgckwb/richlog.git
```

## Quick Start

### The Simplest Way

```python
from richlog import setup_rich_logger

# Quick setup with presets
logger = setup_rich_logger("myapp", preset="production")
logger.info("Application started!")
```

### Basic Usage

```python
from richlog import get_rich_logger, LogFormat, DateFormat, INFO

# Create a simple logger
logger = get_rich_logger("my_app")
logger.info("Hello, RichLog!")

# Create a detailed logger with Enum-based configuration
logger = get_rich_logger(
    name="detailed_app",
    level=INFO,
    log_format=LogFormat.DETAILED,
    date_format=DateFormat.ISO8601
)

logger.debug("Debug information")
logger.info("Application started")
logger.warning("This is a warning")
logger.error("An error occurred")
```

### Using Configuration Files

```python
from richlog import load_settings

# Load from configuration file and create logger
settings = load_settings(Path("richlog.toml"))
logger = settings.create_logger("myapp")

# Or use environment variables
# RICHLOG_LEVEL=DEBUG
# RICHLOG_FORMAT=DETAILED
logger = load_settings().create_logger("myapp")
```

### Shortcuts for Common Patterns

```python
from richlog import setup_file_logger, setup_json_logger

# File logger with rotation
file_logger = setup_file_logger(
    "myapp",
    filename="app.log",
    max_bytes=10_000_000,  # 10MB
    backup_count=5
)

# JSON logger for structured logging
json_logger = setup_json_logger(
    "myapp",
    buffered=True,
    buffer_size=100
)
```

## Advanced Features

### Handlers

```python
from richlog import FileHandler, JSONHandler, AsyncHandler, BufferedHandler

logger = get_rich_logger("my_app")

# File handler with rotation
file_handler = FileHandler(
    "app.log",
    max_bytes=10_000_000,  # 10MB
    backup_count=5
)
logger.addHandler(file_handler)

# JSON handler for structured logging
json_handler = JSONHandler()
logger.addHandler(json_handler)

# Async handler for non-blocking logging
async_handler = AsyncHandler(base_handler=file_handler)
logger.addHandler(async_handler)

# Buffered handler for batch processing
buffered_handler = BufferedHandler(
    base_handler=json_handler,
    buffer_size=100
)
logger.addHandler(buffered_handler)
```

### Decorators

```python
from richlog import log_execution_time, log_errors

logger = get_rich_logger("my_app")

@log_execution_time(logger=logger)
def slow_function():
    time.sleep(1)
    return "Done!"

@log_errors(logger=logger, reraise=False)
def risky_function():
    raise ValueError("Something went wrong")
    # Error will be logged but not raised
```

### Context Manager

```python
from richlog import log_context, INFO, DEBUG

logger = get_rich_logger("my_app", level=INFO)

# Temporarily enable debug logging
with log_context(logger, level=DEBUG):
    logger.debug("This debug message will be shown")
    
logger.debug("This debug message will NOT be shown")
```

## Configuration

RichLog supports multiple configuration methods with validation:

### Environment Variables

```bash
export RICHLOG_LEVEL=DEBUG
export RICHLOG_FORMAT=DETAILED
export RICHLOG_DATE_FORMAT=ISO8601
export RICHLOG_RICH_TRACEBACKS=true
export RICHLOG_TRACEBACK_SUPPRESS=pandas,numpy
```

### Configuration Files

Create a `.richlogrc` or `richlog.toml` file:

**TOML format (richlog.toml):**
```toml
[richlog]
level = "INFO"
format = "VERBOSE"
date_format = "ISO8601"
rich_tracebacks = true
traceback_suppress = ["pandas", "numpy"]
```

**INI format (.richlogrc):**
```ini
[richlog]
level = INFO
format = VERBOSE
date_format = ISO8601
rich_tracebacks = true
traceback_suppress = pandas,numpy
```

### Programmatic Configuration

```python
from richlog import Settings, ConfigError

try:
    settings = Settings(
        level="DEBUG",
        format="DETAILED",
        date_format="ISO8601"
    )
    logger = settings.create_logger("myapp")
except ConfigError as e:
    print(f"Configuration error: {e}")
```

## Available Formats

### Log Formats (Enum)

```python
from richlog import LogFormat

# Available formats:
LogFormat.DEFAULT   # "%(message)s"
LogFormat.SIMPLE    # "%(levelname)s: %(message)s"
LogFormat.VERBOSE   # "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LogFormat.DETAILED  # "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
LogFormat.NOTHING   # "" (minimal output)

# Custom formats are also supported
custom_format = "%(levelname)-8s | %(name)s | %(message)s"
logger = get_rich_logger("app", log_format=custom_format)
```

### Date Formats (Enum)

```python
from richlog import DateFormat

# Available formats:
DateFormat.DEFAULT  # "%Y-%m-%d %H:%M:%S"
DateFormat.ISO8601  # "%Y-%m-%dT%H:%M:%S"
DateFormat.US       # "%m/%d/%Y %I:%M:%S %p"
DateFormat.EU       # "%d/%m/%Y %H:%M:%S"
DateFormat.NOTHING  # "" (no timestamps)

# Custom date formats are supported
custom_date = "%Y年%m月%d日 %H時%M分"
logger = get_rich_logger("app", date_format=custom_date)
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/prgckwb/richlog.git
cd richlog

# Install with development dependencies
uv sync --all-extras --dev

# Install pre-commit hooks
uv run pre-commit install
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=richlog --cov-report=term-missing

# Run specific test file
uv run pytest tests/core/test_logger.py -v
```

### Code Quality

```bash
# Run linting
uv run ruff check src/ tests/

# Run formatting
uv run ruff format src/ tests/

# Type checking (when ty is stable)
uv run ty check src/
```

## Project Structure

```
richlog/
├── src/richlog/
│   ├── __init__.py          # Public API
│   ├── core/                # Core functionality
│   │   ├── logger.py        # Main logger function
│   │   ├── formatters.py    # Log and date format enums
│   │   └── handlers.py      # Custom handlers
│   ├── config/              # Configuration management
│   │   ├── settings.py      # Settings with validation
│   │   └── defaults.py      # Default values
│   ├── shortcuts.py         # Convenience functions
│   └── utils/               # Utilities
│       ├── decorators.py    # Helpful decorators
│       └── context.py       # Context managers
├── tests/                   # Comprehensive test suite
├── .github/workflows/       # CI/CD
└── pyproject.toml          # Project configuration
```

## Migration from v0.1.x

The main change in v0.2.0 is the use of Enums for log and date formats:

```python
# Old way (v0.1.x)
from richlog import LogFormat
logger = get_rich_logger("app", log_format=LogFormat.DETAILED)

# New way (v0.2.0) - Same API, but LogFormat is now an Enum
from richlog import LogFormat
logger = get_rich_logger("app", log_format=LogFormat.DETAILED)

# New features in v0.2.0
# 1. Configuration validation
settings = load_settings()  # Validates log levels

# 2. Easy logger creation from settings
logger = settings.create_logger("app")

# 3. Shortcuts for common patterns
logger = setup_rich_logger("app", preset="production")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Rich](https://github.com/Textualize/rich) - For the beautiful console output
- [Ruff](https://github.com/astral-sh/ruff) - For fast Python linting and formatting
- [uv](https://github.com/astral-sh/uv) - For modern Python package management