"""
Heap data structures: MinHeap, MaxHeap, PriorityQueue
"""

from typing import Any, Iterator, Optional, List
import heapq
from .base import AbstractDataStructure


class MinHeap(AbstractDataStructure):
    """Min heap implementation."""

    def __init__(self, data: Optional[List[Any]] = None):
        self._heap = list(data) if data else []
        if data:
            heapq.heapify(self._heap)

    def push(self, item: Any) -> None:
        """Push item onto heap."""
        heapq.heappush(self._heap, item)

    def pop(self) -> Any:
        """Pop and return smallest item."""
        if self.is_empty():
            raise IndexError("Pop from empty heap")
        return heapq.heappop(self._heap)

    def peek(self) -> Any:
        """Return smallest item without removing."""
        if self.is_empty():
            raise IndexError("Peek from empty heap")
        return self._heap[0]

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def size(self) -> int:
        return len(self._heap)

    def clear(self) -> None:
        self._heap.clear()

    def __iter__(self) -> Iterator[Any]:
        return iter(self._heap)

    def __repr__(self) -> str:
        return f"MinHeap({self._heap})"


class MaxHeap(AbstractDataStructure):
    """Max heap implementation."""

    def __init__(self, data: Optional[List[Any]] = None):
        self._heap = list(data) if data else []
        if data:
            heapq.heapify(self._heap)

    def push(self, item: Any) -> None:
        """Push item onto heap (negated for max)."""
        heapq.heappush(self._heap, -item)

    def pop(self) -> Any:
        """Pop and return largest item."""
        if self.is_empty():
            raise IndexError("Pop from empty heap")
        return -heapq.heappop(self._heap)

    def peek(self) -> Any:
        """Return largest item without removing."""
        if self.is_empty():
            raise IndexError("Peek from empty heap")
        return -self._heap[0]

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def size(self) -> int:
        return len(self._heap)

    def clear(self) -> None:
        self._heap.clear()

    def __iter__(self) -> Iterator[Any]:
        return iter([-x for x in self._heap])

    def __repr__(self) -> str:
        return f"MaxHeap({[-x for x in self._heap]})"


class PriorityQueue(AbstractDataStructure):
    """Priority queue implementation using heap."""

    def __init__(self):
        self._heap: List[tuple] = []
        self._entry_finder: dict = {}
        self._counter = 0
        self._removed = set()

    def enqueue(self, item: Any, priority: float = 0) -> None:
        """Add item with priority."""
        if item in self._entry_finder:
            self.remove(item)
        entry = [priority, self._counter, item]
        self._entry_finder[item] = entry
        heapq.heappush(self._heap, entry)
        self._counter += 1

    def dequeue(self) -> Any:
        """Remove and return highest priority item."""
        while self._heap:
            priority, counter, item = heapq.heappop(self._heap)
            if item not in self._removed:
                del self._entry_finder[item]
                return item
        raise IndexError("Dequeue from empty priority queue")

    def remove(self, item: Any) -> None:
        """Remove item from queue."""
        if item in self._entry_finder:
            self._removed.add(item)
            del self._entry_finder[item]

    def __getitem__(self, item: Any) -> float:
        """Get priority of item."""
        if item in self._entry_finder:
            return self._entry_finder[item][0]
        raise KeyError(item)

    def is_empty(self) -> bool:
        return len(self._entry_finder) == 0

    def size(self) -> int:
        return len(self._entry_finder)

    def clear(self) -> None:
        self._heap.clear()
        self._entry_finder.clear()
        self._removed.clear()
        self._counter = 0

    def __contains__(self, item: Any) -> bool:
        return item in self._entry_finder

    def __repr__(self) -> str:
        return f"PriorityQueue(size={self.size()})"
