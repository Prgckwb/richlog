# RichLog
![SS_2024-11-19_at_13-43-22](https://github.com/user-attachments/assets/65671ba9-46ce-4963-81c0-dcdbade1d3a7)

RichLog is a Python library for enhanced logging using the rich capabilities of the `rich` library. It facilitates the setup of visually appealing and highly configurable logging for various levels, from simple messages to detailed debugging information complete with timestamps and code paths.

## Features

- Multiple log formats including simple, verbose, and detailed.
- Configurable date formats, supporting standards like ISO8601 and regional styles.
- Rich visual output, leveraging the `rich` library for aesthetically pleasing logs.
- Customizable logging levels and handlers.

## Installation

You can install RichLog directly from the GitHub repository. Make sure you have `git` installed and use the following command:

```bash
pip install git+https://github.com/prgckwb/richlog.git
```

## Usage

RichLog provides an easy-to-use function `get_rich_logger` to configure your loggers. Here’s a basic example:

```python
from richlog import get_rich_logger, LogFormat, DateFormat

# Create a logger with default settings
logger = get_rich_logger(name="app_logger")

# Log a simple message
logger.info("This is an info log.")

# Create a logger with a detailed format and ISO8601 date format
detailed_logger = get_rich_logger(
    name="detailed_logger",
    level=logging.DEBUG,
    log_format=LogFormat.DETAILED,
    date_format=DateFormat.ISO8601
)

# Log various levels of messages
detailed_logger.debug("This is a debug message.")
detailed_logger.warning("This is a warning message.")
detailed_logger.error("This is an error message.")
```

## API

### `get_rich_logger`

Creates and configures a logger with rich visualization.

#### Parameters:

- `name` (str): The name of the logger.
- `level` (int): Logging level (e.g., `INFO`, `DEBUG`). Defaults to `INFO`.
- `rich_tracebacks` (bool): Enable rich tracebacks for log errors. Defaults to `True`.
- `traceback_suppress` (Optional[List]): Modules to suppress in tracebacks.
- `log_format` (Union[str, LogFormat]): Selects the format for logs (options in `LogFormat`).
- `date_format` (Union[str, DateFormat]): Selects the format for date representation (options in `DateFormat`).

#### Returns:

- `logging.Logger`: Configured logger instance.

## Log Formats Available

- **DEFAULT:** `"%(message)s"`
- **VERBOSE:** `"%(asctime)s - %(name)s - %(levelname)s - %(message)s"`
- **SIMPLE:** `"%(levelname)s: %(message)s"`
- **DETAILED:** `"%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"`
- **NOTHING:** `""` (for minimal output)

## Date Formats Available

- **DEFAULT:** `"%Y-%m-%d %H:%M:%S"`
- **ISO8601:** `"%Y-%m-%dT%H:%M:%S"`
- **US:** `"%m/%d/%Y %I:%M:%S %p"`
- **EU:** `"%d/%m/%Y %H:%M:%S"`
- **NOTHING:** `""` (for timestamps suppression)

## Contribution

Contributions are welcome! Please feel free to open issues or submit pull requests for feature enhancements or bug fixes.

## License

This project is licensed under the MIT License.
