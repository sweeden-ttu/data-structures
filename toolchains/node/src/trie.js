const { TrieNode } = require('./trieNode');

/**
 * Generic trie (data-structures toolchain).
 */
class Trie {
  constructor(root = null) {
    this._root = root;
  }

  get root() {
    return this._root;
  }

  isEmpty() {
    return this._root == null;
  }

  size() {
    if (this._root == null) return 0;
    return this._countNodes(this._root);
  }

  _countNodes(node) {
    let count = 1;
    for (const child of node.children) {
      count += this._countNodes(child);
    }
    return count;
  }
}

module.exports = { Trie, TrieNode };
