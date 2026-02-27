# data-structures

Abstract data structure definitions available across all programming libraries and domains.

## Overview

This repository provides a comprehensive library of abstract data structures that can be used across all programming projects. It follows consistent interfaces and can be integrated with any Python, Ruby, DotNet, Java, TypeScript, JavaScript, Node, Perl, C, C++, Go, Rust, SWIFT, Objective-C, COBOL, and SQL project.

## Features

- **Linear Structures**: Stack, Queue, Deque, List, Array
- **Trie Structures**: Trie, BinaryTrie, BST (see [Trie (Aho–Corasick family)](#trie-aho-corasick-family) below)
- **Graph Structures**: Graph, DirectedGraph, UndirectedGraph  
- **Hash Structures**: HashTable, BloomFilter
- **Heap Structures**: MinHeap, MaxHeap, PriorityQueue

---

## Trie (Aho–Corasick family)

The **trie** in this library is a prefix tree over a finite set of strings (e.g., dictionary words, pattern keys, or configuration/repo names). It also fits the **Aho–Corasick** family of constructions: a trie of patterns that can be augmented with failure links into a finite-state automaton for multi-pattern matching. A full implementation specification aligned with the [Wikipedia Aho–Corasick example](https://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_algorithm#Example) is in [SPEC_AHO_CORASICK_TRIE.md](docs/SPEC_AHO_CORASICK_TRIE.md).

### Trie as an automaton

- A trie over a finite dictionary can be viewed as a **deterministic finite automaton** (more precisely, a deterministic acyclic word automaton). Each node is a state; edges are labeled by symbols; following a key from the root reaches a state that “recognizes” that prefix.
- **Aho–Corasick** takes a trie of patterns and turns it into a full finite-state machine by adding **failure** (fallback) transitions. That machine recognizes all occurrences of any of the patterns in a single pass—a standard example of “trie → automaton” in practice.

In this repo, the trie is not only a data structure for prefix lookup; it acts as:

- A **recognizer** for the language of keys (strings that correspond to valid nodes/targets).
- With a value payload at each node, it behaves like a **transducer**: read a key, end in a state, and emit an “action bundle” (e.g., node metadata and which agent entrypoints to run).

### Root anchor: Trie of blooming directed graphs

The repository’s root anchor is **`Trie_of_blooming_directed_graphs_with_agents_and_filters`**: a trie whose keys are repo names or context-key prefixes (e.g. `owner_hpcc`, `GlobPretect`) and whose values are references to a blooming-directed-graph node plus filter and trigger agents. Everything else (graphs, agents, filters) hangs off this trie. In automata terms, this root trie is the deterministic automaton over configuration strings; the nondeterministic action graph that hangs off it can be verified with an NFA-style model (e.g., an NFA simulator over operational traces). See [TRIE_ROOT_ANCHOR.md](docs/TRIE_ROOT_ANCHOR.md) and the LaTeX docs in `docs/latex/chapters/` for the full design.

### Language-independent data structure (for automata reports)

When specifying the trie independent of language:

- **States**: trie nodes (one per distinct prefix).
- **Alphabet**: symbols used in keys (e.g., characters or tokens).
- **Transitions**: from each node, one outgoing edge per symbol in the alphabet that continues a key (deterministic).
- **Accepting states**: nodes that correspond to a complete key (e.g. `is_end`).
- **Output (optional)**: value or “action bundle” at accepting nodes (transducer behavior).

This matches the usual NFA/DFA vocabulary and supports describing the trie as the automaton that recognizes the set of stored keys (and, with failure links, the Aho–Corasick automaton for multi-pattern matching).

### Clarifications (Aho–Corasick algorithm)

The following clarifies terminology and behavior from the [Wikipedia Aho–Corasick article](https://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_algorithm#Example):

- **Suffix link (blue arc)**: From each node, the suffix link points to the node whose path is the **longest strict suffix** of the current path that exists in the trie. (A strict suffix is a suffix not equal to the full path.) The root has no suffix link. These links allow the automaton to transition on mismatch without backtracking in the input text: when no child matches the current symbol, follow the suffix link and try again until the root.

- **Dictionary-suffix link (green arc)**: From each node, the dictionary-suffix link points to the first node (if any) reachable by following suffix links that is a dictionary entry (`in_dictionary == true`). At each step, after transitioning to a node, the algorithm outputs the current node if it is in the dictionary, then follows dictionary-suffix links to report any other dictionary matches ending at the same position.

- **Complexity**: Construction is linear in the total length of all dictionary strings. Search is linear in the length of the text plus the number of matches. The algorithm makes a **single pass** over the text with **no backtracking**.

- **Example** (Wikipedia): Dictionary D = {a, ab, bab, bc, bca, c, caa}. On input `abccab`, the algorithm reports (pattern, 1-based end index): a:1, ab:2, bc:3, c:3, c:4, a:5, ab:6. Implementations should reproduce this for the same D and text; see [`spec.js`](spec.js) for a machine-readable test specification.

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

# Binary Search Trie
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
