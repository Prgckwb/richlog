# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

richlog is a Python logging library that enhances the standard logging module with rich console output using the `rich` library. It provides type-safe formatting options, advanced handlers, and flexible configuration management.

## Commands

### Development Setup

```bash
# Install development dependencies
uv sync --all-extras --dev
```

### Testing

```bash
# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=richlog --cov-report=term-missing

# Run specific test file
uv run pytest tests/core/test_logger.py -v

# Run tests matching a pattern
uv run pytest -k "test_logger"
```

### Linting and Formatting

```bash
# Check code style
uv run ruff check src/ tests/

# Format code
uv run ruff format src/ tests/

# Type checking (when ty becomes stable)
uv run ty check src/
```

## Architecture

### Core Design Pattern

The library follows a modular architecture with clear separation of concerns:

1. **Core Module** (`src/richlog/core/`):
   - `logger.py`: Main factory function `setup_rich_logger()` creates configured loggers
   - `formatters.py`: Type-safe Enums (LogFormat, DateFormat) define available formatting options
   - `handlers.py`: Custom handlers extend Python's standard handlers with rich formatting

2. **Configuration System** (`src/richlog/config/`):
   - `settings.py`: Validates and manages configuration from multiple sources (env vars, files, code)
   - `defaults.py`: Defines default values and supported file formats
   - Configuration priority: Code > Environment Variables > Config Files > Defaults

3. **Shortcuts Module** (`src/richlog/shortcuts.py`):
   - Provides high-level functions like `setup_logger_with_preset()` for quick setup
   - Implements preset configurations (e.g., "production", "development")

4. **Utilities** (`src/richlog/utils/`):
   - `decorators.py`: Function decorators for timing and error catching
   - `context.py`: Context managers for temporary logger configuration changes

### Key Design Decisions

1. **Type Safety**: Uses Enums for all format options to ensure type safety and IDE support
2. **Flexible Configuration**: Supports environment variables, TOML/INI files, and programmatic configuration
3. **Handler Architecture**: All custom handlers inherit from standard Python logging handlers, ensuring compatibility
4. **Public API**: Carefully managed through `__init__.py` exports

### Testing Strategy

- Tests mirror the source structure for easy navigation
- Each module has comprehensive unit tests focusing on behavior
- Integration tests verify interactions between components
- Uses pytest fixtures for common test setups
