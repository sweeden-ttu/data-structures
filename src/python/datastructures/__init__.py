"""
datastructures - Abstract Data Structures Library

This module provides abstract data structure definitions that can be used
across all programming projects and toolchains.
"""

from .base import AbstractDataStructure
from .linear import Stack, Queue, Deque, List, Array
from .tree import Tree, BinaryTree, BST, AVLTree, Trie
from .graph import Graph, DirectedGraph, UndirectedGraph
from .hash import HashTable, BloomFilter
from .heap import MinHeap, MaxHeap, PriorityQueue

__version__ = "1.0.0"
__author__ = "sweeden-ttu"

__all__ = [
    "AbstractDataStructure",
    "Stack",
    "Queue",
    "Deque",
    "List",
    "Array",
    "Tree",
    "BinaryTree",
    "BST",
    "AVLTree",
    "Trie",
    "Graph",
    "DirectedGraph",
    "UndirectedGraph",
    "HashTable",
    "BloomFilter",
    "MinHeap",
    "MaxHeap",
    "PriorityQueue",
]
