#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Использовать словарь, содержащий следующие ключи: фамилия и инициалы; номер
# группы; успеваемость (список из 5 элементов). Написать программу, выполняющую
# следующее: ввод с клавиатуры данных в список; записи должны быть упорядочены
# по алфавиту; вывод на дисплей фамилий и номеров групп для всех студентов,
# имеющих хотя бы одну оценку 2; если таких студентов
# нет, вывести соответствующее сообщение.

# Разработайте аналог утилиты tree в Linux. Используйте возможности модуля
# argparse для управления отображением дерева каталогов файловой системы.
# Добавьте дополнительные уникальные возможности в данный программный продукт.

import argparse
import pathlib


def display_tree(directory, args, prefix="", current_depth=0):
    if args.s is not None and current_depth > args.s:
        return

    items = list(directory.iterdir())
    items.sort()

    for idx, item in enumerate(items):
        connector = "├── " if idx < len(items) - 1 else "└── "
        new_prefix = prefix + ("│   " if idx < len(items) - 1 else "    ")

        # Вывести дерево директорий
        if item.is_dir():
            if not args.f:
                print(prefix + connector + item.name + "/")
            display_tree(item, args, new_prefix, current_depth + 1)
        # Вывести дерево только с файлами
        elif item.is_file() and not args.d:
            # Если указан ключ -a, то учитываются скрытые файлы
            if args.a or not item.name.startswith("."):
                size = item.stat().st_size
                # Если ключ -t, то указывать полный путь
                if args.t:
                    print(f"{prefix}{connector}{item} ({size} bytes)")
                else:
                    print(f"{prefix}{connector}{item.name} ({size} bytes)")


def main(command_line=None):
    """Главная функция программы."""
    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version", action="version", version="%(prog)s 0.0.1"
    )
    parser.add_argument("directory", type=str, help="The directory to list.")
    # Выводятся даже скрытые файлы.
    parser.add_argument(
        "-a", action="store_true", help="All files are listed."
    )
    # -f и -d взаимосключащие, так что их нужно запретить вводить одновременно.
    choose = parser.add_mutually_exclusive_group()
    # Отображать каталоги.
    choose.add_argument(
        "-d", action="store_true", help="List directories only."
    )
    # Отображать файлы.
    choose.add_argument("-f", action="store_true", help="List files only.")
    # Максимальная глубина отображения дерева
    parser.add_argument(
        "-s", type=int, help="Max display depth of the directory tree."
    )
    # Не просто имя файла, а полное имя.
    parser.add_argument(
        "-t",
        action="store_true",
        help="Print the full path prefix for each file.",
    )
    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)
    directory = pathlib.Path(args.directory).resolve(strict=True)
    display_tree(directory, args)


if __name__ == "__main__":
    main()
