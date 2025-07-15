# RichLog

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
[![CI](https://github.com/prgckwb/richlog/actions/workflows/ci.yml/badge.svg)](https://github.com/prgckwb/richlog/actions/workflows/ci.yml)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

RichLog is a powerful Python logging library that enhances your logging experience with the rich capabilities of the `rich` library. It provides beautiful, customizable console output with advanced features for production-ready applications.

## Features

- 🎨 **Beautiful Console Output** - Colorful, formatted logs using the `rich` library
- 📝 **Multiple Log Formats** - Simple, verbose, detailed, and custom formats
- 📅 **Flexible Date Formatting** - ISO8601, US, EU, and custom date formats
- 🔧 **Advanced Handlers** - File rotation, JSON output, async logging, and buffered logging
- ⚙️ **Configuration Management** - Environment variables and config file support
- 🎯 **Useful Decorators** - Log execution time and catch errors automatically
- 🔄 **Context Managers** - Temporarily change log levels within code blocks
- 🚀 **Production Ready** - Type hints, comprehensive tests, and CI/CD pipeline

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

### Basic Usage

```python
from richlog import get_rich_logger, LogFormat, DateFormat

# Create a simple logger
logger = get_rich_logger("my_app")
logger.info("Hello, RichLog!")

# Create a detailed logger with custom formatting
logger = get_rich_logger(
    name="detailed_app",
    level=logging.DEBUG,
    log_format=LogFormat.DETAILED,
    date_format=DateFormat.ISO8601
)

logger.debug("Debug information")
logger.info("Application started")
logger.warning("This is a warning")
logger.error("An error occurred")
```

### Advanced Handlers

```python
from richlog.core.handlers import FileHandler, JSONHandler, AsyncHandler, BufferedHandler

# File handler with rotation
file_handler = FileHandler(
    "app.log",
    max_bytes=10_000_000,  # 10MB
    backup_count=5
)

# JSON handler for structured logging
json_handler = JSONHandler()

# Async handler for non-blocking logging
async_handler = AsyncHandler(base_handler=file_handler)

# Buffered handler for batch processing
buffered_handler = BufferedHandler(
    base_handler=json_handler,
    buffer_size=100
)

# Add handlers to your logger
logger = get_rich_logger("my_app")
logger.addHandler(json_handler)
```

### Decorators

```python
from richlog.utils.decorators import log_execution_time, log_errors

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
from richlog.utils.context import log_context
import logging

logger = get_rich_logger("my_app", level=logging.INFO)

# Temporarily enable debug logging
with log_context(logger, level=logging.DEBUG):
    logger.debug("This debug message will be shown")
    
logger.debug("This debug message will NOT be shown")
```

## Configuration

RichLog supports multiple configuration methods:

### Environment Variables

```bash
export RICHLOG_LEVEL=DEBUG
export RICHLOG_FORMAT=DETAILED
export RICHLOG_DATE_FORMAT=ISO8601
export RICHLOG_RICH_TRACEBACKS=true
export RICHLOG_TRACEBACK_SUPPRESS=module1,module2
```

### Configuration Files

Create a `.richlogrc` or `richlog.toml` file:

**INI format (.richlogrc):**
```ini
[richlog]
level = INFO
format = VERBOSE
date_format = ISO8601
rich_tracebacks = true
traceback_suppress = pandas,numpy
```

**TOML format (richlog.toml):**
```toml
[richlog]
level = "INFO"
format = "VERBOSE"
date_format = "ISO8601"
rich_tracebacks = true
traceback_suppress = ["pandas", "numpy"]
```

### Loading Configuration

```python
from richlog.config.settings import load_settings
from richlog import get_rich_logger

# Load settings from file and environment
settings = load_settings(config_path=Path(".richlogrc"))

# Create logger with settings
logger = get_rich_logger(
    "my_app",
    level=settings.get_log_level(),
    log_format=settings.format,
    date_format=settings.date_format,
    rich_tracebacks=settings.rich_tracebacks,
    traceback_suppress=settings.traceback_suppress
)
```

## Available Formats

### Log Formats

- **DEFAULT**: `"%(message)s"`
- **SIMPLE**: `"%(levelname)s: %(message)s"`
- **VERBOSE**: `"%(asctime)s - %(name)s - %(levelname)s - %(message)s"`
- **DETAILED**: `"%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"`
- **NOTHING**: `""` (minimal output)

### Date Formats

- **DEFAULT**: `"%Y-%m-%d %H:%M:%S"`
- **ISO8601**: `"%Y-%m-%dT%H:%M:%S"`
- **US**: `"%m/%d/%Y %I:%M:%S %p"`
- **EU**: `"%d/%m/%Y %H:%M:%S"`
- **NOTHING**: `""` (no timestamps)

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
│   │   ├── formatters.py    # Log and date formats
│   │   └── handlers.py      # Custom handlers
│   ├── config/              # Configuration management
│   │   ├── settings.py      # Settings loader
│   │   └── defaults.py      # Default values
│   └── utils/               # Utilities
│       ├── decorators.py    # Helpful decorators
│       └── context.py       # Context managers
├── tests/                   # Test suite
├── .github/workflows/       # CI/CD
└── pyproject.toml          # Project configuration
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