"""Построчная фильтрация текстового файла."""

from collections.abc import Iterator
from pathlib import Path


def filter_file_lines(
    path: str | Path, keyword: str, *, ignore_case: bool = False
) -> Iterator[str]:
    """Выдаёт строки UTF-8 файла с подстрокой keyword без перевода строки."""
    if not keyword:
        raise ValueError("Строка поиска не должна быть пустой")
    needle = keyword.casefold() if ignore_case else keyword

    with Path(path).open(encoding="utf-8") as source:
        for line in source:
            searchable_line = line.casefold() if ignore_case else line
            if needle in searchable_line:
                yield line.rstrip("\r\n")
