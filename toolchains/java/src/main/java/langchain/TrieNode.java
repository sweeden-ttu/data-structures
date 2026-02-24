package langchain;

import java.util.ArrayList;
import java.util.List;

/** Node for trie structures (LangChain namespace: chain/trie structures). */
public class TrieNode<T> {
    public final T value;
    public final List<TrieNode<T>> children;

    public TrieNode(T value, List<TrieNode<T>> children) {
        this.value = value;
        this.children = children != null ? children : new ArrayList<>();
    }

    public TrieNode(T value) {
        this(value, new ArrayList<>());
    }
}
