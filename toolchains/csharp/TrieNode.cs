namespace LangChain;

/// <summary>Node for trie structures (LangChain namespace: chain/trie structures).</summary>
public class TrieNode<T>
{
    public T Value { get; set; }
    public List<TrieNode<T>> Children { get; } = new();

    public TrieNode(T value, List<TrieNode<T>>? children = null)
    {
        Value = value;
        if (children != null)
            Children.AddRange(children);
    }
}
