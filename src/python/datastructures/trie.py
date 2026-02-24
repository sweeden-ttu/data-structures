"""
Trie data structures: Trie, BinaryTrie, BST, AVLTrie, Trie
"""

from typing import Any, Iterator, Optional, List
from collections import deque
from .base import AbstractDataStructure


class TrieNode:
    """Node for trie structures."""

    def __init__(self, value: Any, children: Optional[List["TrieNode"]] = None):
        self.value = value
        self.children = children or []


class Trie(AbstractDataStructure):
    """Generic trie data structure."""

    def __init__(self, root: Optional[TrieNode] = None):
        self._root = root

    @property
    def root(self) -> Optional[TrieNode]:
        return self._root

    def is_empty(self) -> bool:
        return self._root is None

    def size(self) -> int:
        if self._root is None:
            return 0
        return self._count_nodes(self._root)

    def _count_nodes(self, node: TrieNode) -> int:
        count = 1
        for child in node.children:
            count += self._count_nodes(child)
        return count

    def clear(self) -> None:
        self._root = None

    def depth(self) -> int:
        if self._root is None:
            return 0
        return self._node_depth(self._root)

    def _node_depth(self, node: TrieNode) -> int:
        if not node.children:
            return 1
        return 1 + max(self._node_depth(child) for child in node.children)

    def __iter__(self) -> Iterator[Any]:
        if self._root:
            yield from self._traverse(self._root)

    def _traverse(self, node: TrieNode) -> Iterator[Any]:
        yield node.value
        for child in node.children:
            yield from self._traverse(child)

    def __repr__(self) -> str:
        return f"Trie(root={self._root})"


class BinaryTrieNode:
    """Node for binary trie structures."""

    def __init__(
        self,
        value: Any,
        left: Optional["BinaryTrieNode"] = None,
        right: Optional["BinaryTrieNode"] = None,
    ):
        self.value = value
        self.left = left
        self.right = right


class BinaryTrie(AbstractDataStructure):
    """Generic binary trie data structure."""

    def __init__(self, root: Optional[BinaryTrieNode] = None):
        self._root = root

    @property
    def root(self) -> Optional[BinaryTrieNode]:
        return self._root

    def is_empty(self) -> bool:
        return self._root is None

    def size(self) -> int:
        if self._root is None:
            return 0
        return self._count_nodes(self._root)

    def _count_nodes(self, node: BinaryTrieNode) -> int:
        if node is None:
            return 0
        return 1 + self._count_nodes(node.left) + self._count_nodes(node.right)

    def clear(self) -> None:
        self._root = None

    def height(self) -> int:
        return self._node_height(self._root)

    def _node_height(self, node: Optional[BinaryTrieNode]) -> int:
        if node is None:
            return 0
        return 1 + max(self._node_height(node.left), self._node_height(node.right))

    def inorder(self) -> Iterator[Any]:
        """Inorder traversal."""
        yield from self._inorder(self._root)

    def _inorder(self, node: Optional[BinaryTrieNode]) -> Iterator[Any]:
        if node:
            yield from self._inorder(node.left)
            yield node.value
            yield from self._inorder(node.right)

    def preorder(self) -> Iterator[Any]:
        """Preorder traversal."""
        yield from self._preorder(self._root)

    def _preorder(self, node: Optional[BinaryTrieNode]) -> Iterator[Any]:
        if node:
            yield node.value
            yield from self._preorder(node.left)
            yield from self._preorder(node.right)

    def postorder(self) -> Iterator[Any]:
        """Postorder traversal."""
        yield from self._postorder(self._root)

    def _postorder(self, node: Optional[BinaryTrieNode]) -> Iterator[Any]:
        if node:
            yield from self._postorder(node.left)
            yield from self._postorder(node.right)
            yield node.value

    def level_order(self) -> Iterator[Any]:
        """Level order (BFS) traversal."""
        if self._root is None:
            return
        queue = deque([self._root])
        while queue:
            node = queue.popleft()
            yield node.value
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    def __iter__(self) -> Iterator[Any]:
        yield from self.inorder()

    def __repr__(self) -> str:
        return f"BinaryTrie(root={self._root})"


class BSTNode:
    """Node for Binary Search Trie."""

    def __init__(self, value: Any):
        self.value = value
        self.left: Optional[BSTNode] = None
        self.right: Optional[BSTNode] = None


class BST(AbstractDataStructure):
    """Binary Search Trie."""

    def __init__(self):
        self._root: Optional[BSTNode] = None
        self._size = 0

    def insert(self, value: Any) -> None:
        """Insert value into BST."""
        if self._root is None:
            self._root = BSTNode(value)
            self._size += 1
        else:
            self._insert(self._root, value)

    def _insert(self, node: BSTNode, value: Any) -> None:
        if value < node.value:
            if node.left is None:
                node.left = BSTNode(value)
                self._size += 1
            else:
                self._insert(node.left, value)
        elif value > node.value:
            if node.right is None:
                node.right = BSTNode(value)
                self._size += 1
            else:
                self._insert(node.right, value)

    def search(self, value: Any) -> bool:
        """Search for value in BST."""
        return self._search(self._root, value) is not None

    def _search(self, node: Optional[BSTNode], value: Any) -> Optional[BSTNode]:
        if node is None or node.value == value:
            return node
        if value < node.value:
            return self._search(node.left, value)
        return self._search(node.right, value)

    def delete(self, value: Any) -> None:
        """Delete value from BST."""
        self._root = self._delete(self._root, value)

    def _delete(self, node: Optional[BSTNode], value: Any) -> Optional[BSTNode]:
        if node is None:
            return None
        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            if node.left is None:
                self._size -= 1
                return node.right
            if node.right is None:
                self._size -= 1
                return node.left
            node.value = self._min_value(node.right)
            node.right = self._delete(node.right, node.value)
        return node

    def _min_value(self, node: BSTNode) -> Any:
        current = node
        while current.left:
            current = current.left
        return current.value

    def min(self) -> Optional[Any]:
        """Return minimum value."""
        if self._root is None:
            return None
        node = self._root
        while node.left:
            node = node.left
        return node.value

    def max(self) -> Optional[Any]:
        """Return maximum value."""
        if self._root is None:
            return None
        node = self._root
        while node.right:
            node = node.right
        return node.value

    def is_empty(self) -> bool:
        return self._size == 0

    def size(self) -> int:
        return self._size

    def clear(self) -> None:
        self._root = None
        self._size = 0

    def __contains__(self, value: Any) -> bool:
        return self.search(value)

    def __iter__(self) -> Iterator[Any]:
        yield from BinaryTrie(self._root).inorder()

    def __repr__(self) -> str:
        return f"BST(size={self._size})"


class TrieNode:
    """Node for Trie (prefix trie)."""

    def __init__(self):
        self.children: dict = {}
        self.is_end: bool = False
        self.value: Any = None


class Trie(AbstractDataStructure):
    """Trie (prefix trie) for string operations."""

    def __init__(self):
        self._root = TrieNode()
        self._size = 0

    def insert(self, word: str, value: Any = None) -> None:
        """Insert word into Trie."""
        node = self._root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        if not node.is_end:
            self._size += 1
        node.is_end = True
        node.value = value

    def search(self, word: str) -> bool:
        """Search for exact word."""
        node = self._search_node(word)
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> bool:
        """Check if any word starts with prefix."""
        return self._search_node(prefix) is not None

    def _search_node(self, prefix: str) -> Optional[TrieNode]:
        node = self._root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def get(self, word: str) -> Any:
        """Get value for word."""
        node = self._search_node(word)
        if node and node.is_end:
            return node.value
        return None

    def delete(self, word: str) -> None:
        """Delete word from Trie."""
        self._delete(self._root, word, 0)

    def _delete(self, node: TrieNode, word: str, depth: int) -> bool:
        if node is None:
            return False
        if depth == len(word):
            if node.is_end:
                node.is_end = False
                self._size -= 1
            return len(node.children) == 0
        char = word[depth]
        if char in node.children:
            should_delete = self._delete(node.children[char], word, depth + 1)
            if should_delete:
                del node.children[char]
                return len(node.children) == 0 and not node.is_end
        return False

    def autocomplete(self, prefix: str) -> List[str]:
        """Return all words starting with prefix."""
        node = self._search_node(prefix)
        if node is None:
            return []
        results = []
        self._collect_words(node, prefix, results)
        return results

    def _collect_words(self, node: TrieNode, prefix: str, results: List[str]) -> None:
        if node.is_end:
            results.append(prefix)
        for char, child in node.children.items():
            self._collect_words(child, prefix + char, results)

    def is_empty(self) -> bool:
        return self._size == 0

    def size(self) -> int:
        return self._size

    def clear(self) -> None:
        self._root = TrieNode()
        self._size = 0

    def __contains__(self, word: str) -> bool:
        return self.search(word)

    def __repr__(self) -> str:
        return f"Trie(size={self._size})"
