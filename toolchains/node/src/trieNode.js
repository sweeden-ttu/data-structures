/**
 * Node for trie structures (data-structures toolchain).
 */
class TrieNode {
  constructor(value, children = []) {
    this.value = value;
    this.children = Array.isArray(children) ? children : [];
  }
}

module.exports = { TrieNode };
