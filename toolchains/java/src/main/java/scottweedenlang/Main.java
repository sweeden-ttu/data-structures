package scottweedenlang;

import langchain.Trie;
import langchain.TrieNode;

/** Entry point for data-structures Java toolchain (ScottWeedenLang namespace). */
public class Main {
    public static void main(String[] args) {
        TrieNode<String> root = new TrieNode<>("root");
        root.children.add(new TrieNode<>("a"));
        root.children.add(new TrieNode<>("b"));
        Trie<String> trie = new Trie<>(root);
        System.out.println("Data structures (Java toolchain): trie size = " + trie.size());
    }
}
