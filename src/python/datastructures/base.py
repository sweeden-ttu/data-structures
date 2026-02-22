"""
Base abstract data structure interface.
"""

from abc import ABC, abstractmethod
from typing import Any, Iterator, Optional


class AbstractDataStructure(ABC):
    """
    Abstract base class for all data structures.

    All concrete data structure implementations should inherit from this class
    and implement the required methods.
    """

    @abstractmethod
    def is_empty(self) -> bool:
        """Check if the data structure is empty."""
        pass

    @abstractmethod
    def size(self) -> int:
        """Return the number of elements in the data structure."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Remove all elements from the data structure."""
        pass

    def __len__(self) -> int:
        """Return the size of the data structure."""
        return self.size()

    def __bool__(self) -> bool:
        """Return True if the data structure is not empty."""
        return not self.is_empty()

    def __iter__(self) -> Iterator[Any]:
        """Iterate over elements in the data structure."""
        return iter([])

    def __contains__(self, item: Any) -> bool:
        """Check if item is in the data structure."""
        return False
