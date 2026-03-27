from collections import deque
from typing import List


class BotMemory:
    def __init__(self, max_entries: int = 10):
        self._entries: deque = deque(maxlen=max_entries)

    def add(self, turn: int, description: str) -> None:
        self._entries.append(f"Turn {turn}: {description}")

    def get_entries(self) -> List[str]:
        return list(self._entries)

    def clear(self) -> None:
        self._entries.clear()
