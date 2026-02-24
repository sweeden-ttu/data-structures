package langchain;

/** Generic trie (LangChain namespace: chain/trie structures). */
public class Trie<T> {
    private TrieNode<T> root;

    public Trie(TrieNode<T> root) {
        this.root = root;
    }

    public Trie() {
        this(null);
    }

    public TrieNode<T> getRoot() { return root; }
    public boolean isEmpty() { return root == null; }

    public int size() {
        if (root == null) return 0;
        return countNodes(root);
    }

    private int countNodes(TrieNode<T> node) {
        int count = 1;
        for (TrieNode<T> child : node.children) {
            count += countNodes(child);
        }
        return count;
    }
}
