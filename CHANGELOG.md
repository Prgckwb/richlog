# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Complete project restructure with modular architecture
- Advanced handlers: FileHandler, JSONHandler, AsyncHandler, BufferedHandler
- Configuration management with environment variables and config files support
- Utility decorators: `@log_execution_time` and `@log_errors`
- Context manager `log_context` for temporary log level changes
- Comprehensive test suite with 89% code coverage
- Development tools: ruff, pre-commit hooks, GitHub Actions CI/CD
- Type hints throughout the codebase
- Support for Python 3.9+

### Changed
- Moved core functionality to modular structure (core, config, utils)
- Improved error handling and logging patterns
- Updated documentation with extensive examples

### Fixed
- Handler cleanup in AsyncHandler
- Buffer deadlock issue in BufferedHandler

## [0.1.0] - 2024-11-19

### Added
- Initial release
- Basic rich logging functionality
- Multiple log formats (DEFAULT, SIMPLE, VERBOSE, DETAILED)
- Date format options (ISO8601, US, EU)
- Rich tracebacks support
- Basic documentation and examples