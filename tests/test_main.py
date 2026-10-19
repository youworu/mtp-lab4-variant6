"""Проверки реального консольного запуска программы."""

import os
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class CommandLineTests(unittest.TestCase):
    """Команды, результаты и обработка неверных аргументов."""

    def run_command(self, *arguments):
        environment = os.environ.copy()
        environment["PYTHONIOENCODING"] = "utf-8"
        return subprocess.run(
            [sys.executable, "main.py", *arguments],
            cwd=PROJECT_ROOT,
            env=environment,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=10,
        )

    def test_primes_command_also_reports_elapsed_time(self):
        result = self.run_command("primes", "--limit", "10")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "[2, 3, 5, 7]")
        self.assertRegex(result.stderr, r"collect_primes: \d+\.\d{6} с")

    def test_even_numbers_command(self):
        result = self.run_command("evens", "-4", "-3", "0", "1", "2", "2")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "[-4, 0, 2, 2]")

    def test_even_numbers_command_accepts_empty_input(self):
        result = self.run_command("evens")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "[]")

    def test_file_filter_command(self):
        result = self.run_command("filter-file", "examples/events.txt", "ERROR")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout.splitlines(),
            ["ERROR: Не удалось открыть файл", "ERROR: Некорректный номер группы"],
        )

    def test_file_filter_command_ignores_case_when_requested(self):
        result = self.run_command(
            "filter-file", "examples/events.txt", "ERROR", "--ignore-case"
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(result.stdout.splitlines()), 3)
        self.assertIn("error: Временная ошибка сети", result.stdout)

    def test_reduce_commands(self):
        cases = (
            (("reduce", "1", "2", "3", "4"), "10"),
            (("reduce", "1", "2", "3", "4", "--operation", "product"), "24"),
            (("reduce", "1", "2", "--initial", "10"), "13"),
            (("reduce", "--initial", "0"), "0"),
        )
        for arguments, expected in cases:
            with self.subTest(arguments=arguments):
                result = self.run_command(*arguments)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout.strip(), expected)

    def test_demo_runs_all_examples(self):
        result = self.run_command("demo")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(
            "Простые числа до 30: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]",
            result.stdout,
        )
        self.assertIn("Чётные числа: [-4, 0, 2, 4]", result.stdout)
        self.assertIn("Сумма через reduce: 10", result.stdout)
        self.assertIn("Произведение через reduce: 24", result.stdout)
        self.assertIn("ERROR: Не удалось открыть файл", result.stdout)

    def test_invalid_input_reports_an_error(self):
        cases = (
            (),
            ("primes", "--limit", "-1"),
            ("primes", "--limit", "abc"),
            ("evens", "abc"),
            ("filter-file", "missing.txt", "ERROR"),
            ("filter-file", "examples/events.txt", ""),
            ("reduce",),
            ("reduce", "1", "--operation", "unknown"),
        )
        for arguments in cases:
            with self.subTest(arguments=arguments):
                result = self.run_command(*arguments)
                self.assertEqual(result.returncode, 2)
                self.assertIn("error:", result.stderr)
                self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
