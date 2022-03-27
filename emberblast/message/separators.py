import multiprocessing
import os
import time
from typing import List

from termcolor import colored


def print_line_separator():
    term_size = os.get_terminal_size()
    print(u'\u2500' * term_size.columns)


def print_loading(prefix: str, prefix_attributes: List[str]) -> None:
    animation = [
        "        ",
        ".       ",
        "..     ",
        "...     ",
        "....    ",
        ".....   ",
        "......  ",
        "....... ",
        "........",
        " .......",
        "  ......",
        "   .....",
        "    ....",
        "     ...",
        "      ..",
        "       .",
        "        ",
        "        "
    ]

    notcomplete = True

    i = 0

    while notcomplete:
        print(colored(prefix + animation[i % len(animation)], 'green', prefix_attributes), end='\r')
        time.sleep(.1)
        i += 1


def execute_loading(loading_time: int, prefix: str, prefix_attributes: List[str]) -> None:
    p = multiprocessing.Process(target=print_loading(prefix, prefix_attributes))
    p.start()

    # Wait for 10 seconds or until process finishes
    p.join(loading_time)

    # If thread is still active
    if p.is_alive():
        p.kill()
