import argparse
import os
import re


def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="dep-graph-tool",
        description="Инструмент визуализации графа зависимостей (Вариант 27)",
    )

    parser.add_argument(
        "-p", "--package",
        required=True,
        help="Имя анализируемого пакета"
    )
    parser.add_argument(
        "-r", "--repo",
        required=True,
        help="URL-адрес репозитория или путь к файлу тестового репозитория"
    )
    parser.add_argument(
        "-m", "--mode",
        choices=["url", "file"],
        required=True,
        help="Режим работы с тестовым репозиторием (url или file)"
    )
    parser.add_argument(
        "-v", "--version",
        required=True,
        help="Версия пакета"
    )
    parser.add_argument(
        "-o", "--output",
        default="graph.png",
        help="Имя сгенерированного файла с изображением графа"
    )
    parser.add_argument(
        "-a", "--ascii",
        action="store_true",
        help="Режим вывода зависимостей в формате ASCII-дерева"
    )

    return parser.parse_args(argv)


def validate_config(args: argparse.Namespace) -> None:
    if not args.package.strip():
        raise ValueError("Имя пакета не может быть пустым.")

    if args.mode == "file":
        if not os.path.exists(args.repo):
            raise FileNotFoundError(f"Файл тестового репозитория не найден:"
                                    f" {args.repo}")
    elif args.mode == "url":
        if not (args.repo.startswith("http://") or
                args.repo.startswith("https://")):
            raise ValueError(f"Некорректный URL репозитория: {args.repo}")

    if not re.match(r"^\d+\.\d+(\.\d+)?$", args.version):
        raise ValueError(f"Неверный формат версии '{args.version}'. "
                         f"Ожидается, например, 1.0.0")

    if not args.output.lower().endswith(".png"):
        raise ValueError(f"Файл графа должен иметь расширение .png, получено:"
                         f" {args.output}")


def print_config(args: argparse.Namespace) -> None:
    print("Параметры запуска")
    print(f"Анализируемый пакет : {args.package}")
    print(f"Репозиторий         : {args.repo}")
    print(f"Режим работы        : {args.mode}")
    print(f"Версия пакета       : {args.version}")
    print(f"Выходной файл графа : {args.output}")
    print(f"ASCII-дерево        : {'Включено' if args.ascii else 
    'Выключено'}")