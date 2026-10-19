"""Свёртка последовательности без вызова functools.reduce."""

from collections.abc import Callable, Iterable
from typing import Any


_MISSING = object()


def custom_reduce(
    function: Callable[[Any, Any], Any],
    iterable: Iterable[Any],
    initial: Any = _MISSING,
) -> Any:
    """Сворачивает iterable слева направо, учитывая необязательный initial."""
    iterator = iter(iterable)
    if initial is _MISSING:
        try:
            result = next(iterator)
        except StopIteration:
            raise TypeError(
                "Пустая последовательность без начального значения"
            ) from None
    else:
        result = initial

    for item in iterator:
        result = function(result, item)
    return result
