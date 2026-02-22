"""
Hash-based data structures: HashTable, BloomFilter
"""

from typing import Any, Iterator, Optional, List
import hashlib
from .base import AbstractDataStructure


class HashTable(AbstractDataStructure):
    """Hash table implementation."""

    def __init__(self, size: int = 100):
        self._size = size
        self._table: List[Optional[tuple]] = [None] * size
        self._count = 0

    def _hash(self, key: Any) -> int:
        """Hash function."""
        if isinstance(key, str):
            return int(hashlib.md5(key.encode()).hexdigest(), 16) % self._size
        return hash(key) % self._size

    def insert(self, key: Any, value: Any) -> None:
        """Insert key-value pair."""
        index = self._hash(key)

        if self._table[index] is None:
            self._table[index] = [(key, value)]
        else:
            for i, (k, v) in enumerate(self._table[index]):
                if k == key:
                    self._table[index][i] = (key, value)
                    return
            self._table[index].append((key, value))

        self._count += 1

        if self._count / self._size > 0.75:
            self._resize()

    def _resize(self) -> None:
        """Resize the hash table."""
        old_table = self._table
        self._size *= 2
        self._table = [None] * self._size
        self._count = 0

        for bucket in old_table:
            if bucket:
                for key, value in bucket:
                    self.insert(key, value)

    def get(self, key: Any, default: Any = None) -> Any:
        """Get value for key."""
        index = self._hash(key)
        bucket = self._table[index]

        if bucket is None:
            return default

        for k, v in bucket:
            if k == key:
                return v
        return default

    def delete(self, key: Any) -> None:
        """Delete key-value pair."""
        index = self._hash(key)
        bucket = self._table[index]

        if bucket is None:
            return

        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self._count -= 1
                return

    def __setitem__(self, key: Any, value: Any) -> None:
        self.insert(key, value)

    def __getitem__(self, key: Any) -> Any:
        result = self.get(key)
        if result is None:
            raise KeyError(key)
        return result

    def __delitem__(self, key: Any) -> None:
        self.delete(key)

    def is_empty(self) -> bool:
        return self._count == 0

    def size(self) -> int:
        return self._count

    def clear(self) -> None:
        self._table = [None] * self._size
        self._count = 0

    def keys(self) -> List[Any]:
        """Return all keys."""
        result = []
        for bucket in self._table:
            if bucket:
                result.extend(k for k, v in bucket)
        return result

    def values(self) -> List[Any]:
        """Return all values."""
        result = []
        for bucket in self._table:
            if bucket:
                result.extend(v for k, v in bucket)
        return result

    def items(self) -> List[tuple]:
        """Return all key-value pairs."""
        result = []
        for bucket in self._table:
            if bucket:
                result.extend(bucket)
        return result

    def __contains__(self, key: Any) -> bool:
        return self.get(key) is not None

    def __iter__(self) -> Iterator[Any]:
        return iter(self.keys())

    def __len__(self) -> int:
        return self._count

    def __repr__(self) -> str:
        return f"HashTable(size={self._count})"


class BloomFilter(AbstractDataStructure):
    """Bloom filter for membership testing."""

    def __init__(self, size: int = 1000, hash_count: int = 3):
        self._size = size
        self._hash_count = hash_count
        self._bits = [False] * size
        self._count = 0

    def _hashes(self, item: str) -> List[int]:
        """Generate hash values."""
        result = []
        for i in range(self._hash_count):
            hash_str = f"{item}{i}".encode()
            hash_val = int(hashlib.md5(hash_str).hexdigest(), 16)
            result.append(hash_val % self._size)
        return result

    def add(self, item: str) -> None:
        """Add item to bloom filter."""
        for index in self._hashes(item):
            self._bits[index] = True
        self._count += 1

    def contains(self, item: str) -> bool:
        """Check if item might be in filter."""
        return all(self._bits[index] for index in self._hashes(item))

    def __setitem__(self, item: str) -> None:
        self.add(item)

    def __contains__(self, item: str) -> bool:
        return self.contains(item)

    def is_empty(self) -> bool:
        return self._count == 0

    def size(self) -> int:
        return self._count

    def clear(self) -> None:
        self._bits = [False] * self._size
        self._count = 0

    def false_positive_rate(self) -> float:
        """Estimate false positive rate."""
        import math

        exponent = -self._hash_count * self._count / self._size
        return (1 - math.exp(exponent)) ** self._hash_count

    def __repr__(self) -> str:
        return f"BloomFilter(size={self._count}, fpr={self.false_positive_rate():.4f})"
