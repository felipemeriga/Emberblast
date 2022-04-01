import multiprocessing
import os
import time
from typing import List

from termcolor import colored


def print_line_separator():
    term_size = os.get_terminal_size()
    print(u'\u2500' * term_size.columns)


animation = [
    "          ",
    ".         ",
    "..        ",
    "...       ",
    "....      ",
    ".....     ",
    "......    ",
    ".......   ",
    "........  ",
    "......... ",
    "..........",
    " .........",
    "  ........",
    "   .......",
    "    ......",
    "     .....",
    "      ....",
    "       ...",
    "        ..",
    "         ."
]


def print_loading() -> None:
    notcomplete = True

    i = 0

    while notcomplete:
        print(animation[i % len(animation)], end='\r')
        time.sleep(.05)
        i += 1


def execute_loading(loading_time: int, prefix: str = '', prefix_attributes: List[str] = None) -> None:
    if prefix != '':
        print(colored(prefix, None, attrs=prefix_attributes))
    p = multiprocessing.Process(target=print_loading)
    p.start()

    p.join(loading_time)

    # If thread is still active
    if p.is_alive():
        p.kill()
        print(" " * len(animation[0]), end="\r")
