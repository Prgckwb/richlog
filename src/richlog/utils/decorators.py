import functools
import logging
import time
from typing import Any, Callable, TypeVar, cast

F = TypeVar("F", bound=Callable[..., Any])


def log_execution_time(
    logger: logging.Logger,
    level: int = logging.INFO,
) -> Callable[[F], F]:
    """Decorator that logs function execution time.

    Args:
        logger: Logger to record the log
        level: Log level (defaults to INFO)

    Returns:
        Decorated function
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                end_time = time.time()
                execution_time = end_time - start_time
                logger.log(
                    level,
                    f"{func.__name__} took {execution_time:.4f} seconds to execute",
                )

        return cast(F, wrapper)

    return decorator


def log_errors(
    logger: logging.Logger,
    level: int = logging.ERROR,
    reraise: bool = True,
) -> Callable[[F], F]:
    """Decorator that logs exceptions raised within a function.

    Args:
        logger: Logger to record the log
        level: Log level (defaults to ERROR)
        reraise: Whether to re-raise the exception (defaults to True)

    Returns:
        Decorated function
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.log(
                    level,
                    f"Error in {getattr(func, '__name__', 'unknown')}: {type(e).__name__}: {e!s}",
                    exc_info=True,
                )
                if reraise:
                    raise
                return None

        return cast(F, wrapper)

    return decorator
