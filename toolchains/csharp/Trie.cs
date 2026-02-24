namespace LangChain;

/// <summary>Generic trie (LangChain namespace: chain/trie structures).</summary>
public class Trie<T>
{
    public TrieNode<T>? Root { get; set; }

    public Trie(TrieNode<T>? root = null) => Root = root;

    public bool IsEmpty => Root == null;

    public int Size => Root == null ? 0 : CountNodes(Root);

    static int CountNodes(TrieNode<T> node)
    {
        int count = 1;
        foreach (var child in node.Children)
            count += CountNodes(child);
        return count;
    }
}
