import functools
import logging
import time
from typing import Any, Callable, TypeVar, cast

F = TypeVar("F", bound=Callable[..., Any])


def log_execution_time(
    logger: logging.Logger,
    level: int = logging.INFO,
) -> Callable[[F], F]:
    """関数の実行時間をログに記録するデコレータ

    Args:
        logger: ログを記録するロガー
        level: ログレベル(デフォルトはINFO)

    Returns:
        デコレートされた関数
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
    """関数内で発生した例外をログに記録するデコレータ

    Args:
        logger: ログを記録するロガー
        level: ログレベル(デフォルトはERROR)
        reraise: 例外を再発生させるかどうか(デフォルトはTrue)

    Returns:
        デコレートされた関数
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.log(
                    level,
                    f"Error in {func.__name__}: {type(e).__name__}: {e!s}",
                    exc_info=True,
                )
                if reraise:
                    raise
                return None

        return cast(F, wrapper)

    return decorator
