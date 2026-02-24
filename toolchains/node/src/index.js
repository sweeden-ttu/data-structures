const { Trie, TrieNode } = require('./trie');

const root = new TrieNode('root', [
  new TrieNode('a'),
  new TrieNode('b'),
]);
const trie = new Trie(root);
console.log('Data structures (Node toolchain): trie size =', trie.size());

module.exports = { Trie, TrieNode };
