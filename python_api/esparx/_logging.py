import sys
from typing import Iterable


def info(text: str):
    print(f"\033[1;38mInfo:\033[0m {text}")


def warning(text: str):
    print(f"\033[1;93mWarning:\033[0m {text}")


def error(text: str):
    print(f"\033[1;91mError:\033[0m {text}")


def progress(it: Iterable, prefix="", size=60, steps=60, unit="", out=sys.stdout):
    def show(j):
        x = int(j / steps * size)
        print(
            "{}[{}{}] {}/{} {}".format(prefix, "#" * x, "." * (size - x), j, steps, unit),
            end="\r",
            file=out,
            flush=True,
        )

    show(0)
    for i, item in enumerate(it):
        yield item
        show(i + 1)
    print("\n", flush=True, file=out)
