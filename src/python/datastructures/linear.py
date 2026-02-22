"""
Linear data structures: Stack, Queue, Deque, List, Array
"""

from typing import Any, Iterator, Optional
from collections import deque as _deque
from .base import AbstractDataStructure


class Stack(AbstractDataStructure):
    """LIFO (Last In First Out) data structure."""

    def __init__(self):
        self._items: list = []

    def push(self, item: Any) -> None:
        """Add an item to the top of the stack."""
        self._items.append(item)

    def pop(self) -> Any:
        """Remove and return the top item."""
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self._items.pop()

    def peek(self) -> Any:
        """Return the top item without removing it."""
        if self.is_empty():
            raise IndexError("Peek from empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def size(self) -> int:
        return len(self._items)

    def clear(self) -> None:
        self._items.clear()

    def __iter__(self) -> Iterator[Any]:
        return iter(reversed(self._items))

    def __repr__(self) -> str:
        return f"Stack({self._items})"


class Queue(AbstractDataStructure):
    """FIFO (First In First Out) data structure."""

    def __init__(self):
        self._items: list = []

    def enqueue(self, item: Any) -> None:
        """Add an item to the back of the queue."""
        self._items.append(item)

    def dequeue(self) -> Any:
        """Remove and return the front item."""
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        return self._items.pop(0)

    def front(self) -> Any:
        """Return the front item without removing it."""
        if self.is_empty():
            raise IndexError("Front of empty queue")
        return self._items[0]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def size(self) -> int:
        return len(self._items)

    def clear(self) -> None:
        self._items.clear()

    def __iter__(self) -> Iterator[Any]:
        return iter(self._items)

    def __repr__(self) -> str:
        return f"Queue({self._items})"


class Deque(AbstractDataStructure):
    """Double-ended queue."""

    def __init__(self):
        self._items: _deque = _deque()

    def add_front(self, item: Any) -> None:
        """Add an item to the front."""
        self._items.appendleft(item)

    def add_back(self, item: Any) -> None:
        """Add an item to the back."""
        self._items.append(item)

    def remove_front(self) -> Any:
        """Remove and return the front item."""
        if self.is_empty():
            raise IndexError("Remove from empty deque")
        return self._items.popleft()

    def remove_back(self) -> Any:
        """Remove and return the back item."""
        if self.is_empty():
            raise IndexError("Remove from empty deque")
        return self._items.pop()

    def front(self) -> Any:
        """Return the front item without removing."""
        if self.is_empty():
            raise IndexError("Front of empty deque")
        return self._items[0]

    def back(self) -> Any:
        """Return the back item without removing."""
        if self.is_empty():
            raise IndexError("Back of empty deque")
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def size(self) -> int:
        return len(self._items)

    def clear(self) -> None:
        self._items.clear()

    def __iter__(self) -> Iterator[Any]:
        return iter(self._items)

    def __repr__(self) -> str:
        return f"Deque({list(self._items)})"


class List(AbstractDataStructure):
    """Dynamic array list implementation."""

    def __init__(self, initial_items: Optional[list] = None):
        self._items: list = list(initial_items) if initial_items else []

    def append(self, item: Any) -> None:
        """Append item to the end."""
        self._items.append(item)

    def insert(self, index: int, item: Any) -> None:
        """Insert item at index."""
        self._items.insert(index, item)

    def remove(self, item: Any) -> None:
        """Remove first occurrence of item."""
        self._items.remove(item)

    def pop(self, index: int = -1) -> Any:
        """Remove and return item at index."""
        return self._items.pop(index)

    def get(self, index: int) -> Any:
        """Get item at index."""
        return self._items[index]

    def set(self, index: int, item: Any) -> None:
        """Set item at index."""
        self._items[index] = item

    def index(self, item: Any) -> int:
        """Return index of first occurrence."""
        return self._items.index(item)

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def size(self) -> int:
        return len(self._items)

    def clear(self) -> None:
        self._items.clear()

    def __getitem__(self, index: int) -> Any:
        return self._items[index]

    def __setitem__(self, index: int, item: Any) -> None:
        self._items[index] = item

    def __iter__(self) -> Iterator[Any]:
        return iter(self._items)

    def __contains__(self, item: Any) -> bool:
        return item in self._items

    def __repr__(self) -> str:
        return f"List({self._items})"


class Array:
    """Fixed-size array implementation."""

    def __init__(self, size: int, default: Any = None):
        if size <= 0:
            raise ValueError("Size must be positive")
        self._size = size
        self._default = default
        self._items: list = [default] * size

    @property
    def size(self) -> int:
        return self._size

    def get(self, index: int) -> Any:
        if not 0 <= index < self._size:
            raise IndexError("Index out of bounds")
        return self._items[index]

    def set(self, index: int, item: Any) -> None:
        if not 0 <= index < self._size:
            raise IndexError("Index out of bounds")
        self._items[index] = item

    def fill(self, item: Any) -> None:
        """Fill array with item."""
        self._items = [item] * self._size

    def __getitem__(self, index: int) -> Any:
        return self.get(index)

    def __setitem__(self, index: int, item: Any) -> None:
        self.set(index, item)

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return f"Array({self._items})"
