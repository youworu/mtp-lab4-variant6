"""Проверки ленивой фильтрации файла и освобождения ресурса."""

import io
import tempfile
import unittest
from pathlib import Path
from types import GeneratorType
from unittest.mock import patch

from file_filter import filter_file_lines


class FileFilterTests(unittest.TestCase):
    """Поиск строк, кодировка, ошибки и закрытие открытого файла."""

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.path = Path(temporary.name) / "events.txt"
        self.path.write_text(
            "INFO: начало\nERROR: ошибка\nerror: другая ошибка\n"
            "  ERROR: строка с пробелами  \nКонец без перевода строки",
            encoding="utf-8",
        )

    def test_returns_a_generator(self):
        self.assertIsInstance(filter_file_lines(self.path, "ERROR"), GeneratorType)

    def test_matches_lines_and_preserves_spaces(self):
        self.assertEqual(
            list(filter_file_lines(self.path, "ERROR")),
            ["ERROR: ошибка", "  ERROR: строка с пробелами  "],
        )

    def test_case_insensitive_search(self):
        self.assertEqual(
            list(filter_file_lines(self.path, "ERROR", ignore_case=True)),
            ["ERROR: ошибка", "error: другая ошибка", "  ERROR: строка с пробелами  "],
        )

    def test_case_insensitive_search_supports_cyrillic(self):
        self.assertEqual(
            list(filter_file_lines(self.path, "КОНЕЦ", ignore_case=True)),
            ["Конец без перевода строки"],
        )

    def test_no_matches_and_empty_file(self):
        self.assertEqual(list(filter_file_lines(self.path, "missing")), [])
        self.path.write_text("", encoding="utf-8")
        self.assertEqual(list(filter_file_lines(self.path, "ERROR")), [])

    def test_rejects_an_empty_keyword(self):
        with self.assertRaises(ValueError):
            list(filter_file_lines(self.path, ""))

    def test_missing_file_is_reported(self):
        with self.assertRaises(FileNotFoundError):
            list(filter_file_lines(self.path.parent / "missing.txt", "ERROR"))

    def test_invalid_utf8_is_reported(self):
        self.path.write_bytes(b"\xff")

        with self.assertRaises(UnicodeDecodeError):
            list(filter_file_lines(self.path, "ERROR"))

    def test_opens_lazily_and_closes_after_partial_consumption(self):
        source = io.StringIO("ERROR: первая\nERROR: вторая\n")
        with patch("file_filter.Path.open", return_value=source) as open_file:
            lines = filter_file_lines(self.path, "ERROR")
            open_file.assert_not_called()
            self.assertEqual(next(lines), "ERROR: первая")
            self.assertFalse(source.closed)
            lines.close()
            self.assertTrue(source.closed)

    def test_closes_after_full_consumption(self):
        source = io.StringIO("ERROR: первая\nINFO: вторая\n")
        with patch("file_filter.Path.open", return_value=source):
            self.assertEqual(
                list(filter_file_lines(self.path, "ERROR")), ["ERROR: первая"]
            )
        self.assertTrue(source.closed)

    def test_reads_one_line_at_a_time(self):
        class IterationOnlyFile(io.StringIO):
            def read(self, *args, **kwargs):
                raise AssertionError("Нельзя читать файл целиком")

            def readlines(self, *args, **kwargs):
                raise AssertionError("Нельзя собирать все строки заранее")

        source = IterationOnlyFile("ERROR: первая\nINFO: вторая\nERROR: третья\n")
        with patch("file_filter.Path.open", return_value=source):
            lines = filter_file_lines(self.path, "ERROR")
            self.assertEqual(next(lines), "ERROR: первая")
            self.assertEqual(source.tell(), len("ERROR: первая\n"))
            lines.close()


if __name__ == "__main__":
    unittest.main()
