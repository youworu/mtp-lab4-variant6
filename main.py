"""Консольные примеры функционального программирования."""

import argparse
import logging
import operator
from pathlib import Path

from file_filter import filter_file_lines
from numbers_tasks import filter_even_numbers, prime_numbers
from reducing import custom_reduce
from timing import time_execution


EXAMPLE_FILE = Path(__file__).resolve().parent / "examples" / "events.txt"


@time_execution
def collect_primes(limit: int) -> list[int]:
    """Получает все простые числа, чтобы замер включал работу генератора."""
    return list(prime_numbers(limit))


def build_parser() -> argparse.ArgumentParser:
    """Описывает команды лабораторной и их аргументы."""
    parser = argparse.ArgumentParser(description="Лабораторная №4, вариант 6")
    commands = parser.add_subparsers(dest="command", required=True)

    primes = commands.add_parser("primes", help="Простые числа до верхней границы")
    primes.add_argument("--limit", type=int, default=30)

    evens = commands.add_parser("evens", help="Отфильтровать чётные числа")
    evens.add_argument("numbers", type=int, nargs="*")

    file_command = commands.add_parser("filter-file", help="Найти строки в UTF-8 файле")
    file_command.add_argument("path", type=Path)
    file_command.add_argument("keyword")
    file_command.add_argument("--ignore-case", action="store_true")

    reduce_command = commands.add_parser("reduce", help="Собственная свёртка чисел")
    reduce_command.add_argument("numbers", type=int, nargs="*")
    reduce_command.add_argument(
        "--operation", choices=("sum", "product"), default="sum"
    )
    reduce_command.add_argument("--initial", type=int)

    commands.add_parser("demo", help="Запустить все примеры")
    return parser


def show_demo() -> None:
    """Показывает все пять заданий на небольших данных."""
    print(f"Простые числа до 30: {collect_primes(30)}")
    numbers = [-4, -3, 0, 1, 2, 3, 4]
    print(f"Чётные числа: {filter_even_numbers(numbers)}")
    print(f"Сумма через reduce: {custom_reduce(operator.add, [1, 2, 3, 4])}")
    print(f"Произведение через reduce: {custom_reduce(operator.mul, [1, 2, 3, 4])}")
    print("Строки с ERROR:")
    for line in filter_file_lines(EXAMPLE_FILE, "ERROR"):
        print(line)


def main() -> None:
    """Запускает команду и выводит ошибки аргументов без traceback."""
    parser = build_parser()
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    try:
        if args.command == "primes":
            print(collect_primes(args.limit))
        elif args.command == "evens":
            print(filter_even_numbers(args.numbers))
        elif args.command == "filter-file":
            for line in filter_file_lines(
                args.path, args.keyword, ignore_case=args.ignore_case
            ):
                print(line)
        elif args.command == "reduce":
            combine = operator.add if args.operation == "sum" else operator.mul
            if args.initial is None:
                print(custom_reduce(combine, args.numbers))
            else:
                print(custom_reduce(combine, args.numbers, args.initial))
        elif args.command == "demo":
            show_demo()
    except UnicodeError:
        parser.error("Файл должен быть сохранён в кодировке UTF-8")
    except (OSError, ValueError, TypeError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
