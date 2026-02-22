# data-structures

Abstract data structure definitions available across all programming libraries and domains.

## Overview

This repository provides a comprehensive library of abstract data structures that can be used across all programming projects. It follows consistent interfaces and can be integrated with any Python, Ruby, DotNet, Java, TypeScript, JavaScript, Node, Perl, C, C++, Go, Rust, SWIFT, Objective-C, COBOL, and SQL project.

## Features

- **Linear Structures**: Stack, Queue, Deque, List, Array
- **Tree Structures**: Tree, BinaryTree, BST, Trie
- **Graph Structures**: Graph, DirectedGraph, UndirectedGraph  
- **Hash Structures**: HashTable, BloomFilter
- **Heap Structures**: MinHeap, MaxHeap, PriorityQueue

## Installation

```bash
pip install datastructures
```

Or install from source:

```bash
cd src/python
pip install -e .
```

## Quick Start

```python
from datastructures import Stack, Queue, BST, Trie, Graph

# Stack
stack = Stack()
stack.push(1)
stack.push(2)
print(stack.pop())  # 2

# Queue
queue = Queue()
queue.enqueue("first")
queue.enqueue("second")
print(queue.dequeue())  # "first"

# Binary Search Tree
bst = BST()
bst.insert(5)
bst.insert(3)
bst.insert(7)
print(5 in bst)  # True

# Trie for prefix matching
trie = Trie()
trie.insert("hello")
trie.insert("help")
print(trie.autocomplete("hel"))  # ["hello", "help"]

# Graph
graph = DirectedGraph()
graph.add_edge("A", "B")
graph.add_edge("B", "C")
print(list(graph.bfs("A")))  # ["A", "B", "C"]
```

## Project Integration

### OllamaHpcc

```python
# Use data structures in OllamaHpcc
from datastructures import Trie, Queue
from ollamahpcc import OllamaClient
```

### GlobPretect

```python
# Use data structures in VPN tunnel management
from datastructures import PriorityQueue, Graph
from globpretect import TunnelManager
```

### brw-scan-print

```python
# Use data structures in printer queue management
from datastructures import Queue, Stack
```

## Documentation

See `docs/` directory for detailed documentation.

## License

MIT License
