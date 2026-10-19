"""Декоратор измерения времени выполнения функции."""

import logging
from collections.abc import Callable
from functools import wraps
from time import perf_counter
from typing import ParamSpec, TypeVar


P = ParamSpec("P")
R = TypeVar("R")
logger = logging.getLogger(__name__)


def time_execution(function: Callable[P, R]) -> Callable[P, R]:
    """Записывает длительность вызова, сохраняя результат и исключения."""
    @wraps(function)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        started_at = perf_counter()
        try:
            return function(*args, **kwargs)
        finally:
            elapsed = perf_counter() - started_at
            logger.info("%s: %.6f с", function.__name__, elapsed)

    return wrapper
