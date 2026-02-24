using LangChain;

var root = new TrieNode<string>("root");
root.Children.Add(new TrieNode<string>("a"));
root.Children.Add(new TrieNode<string>("b"));
var trie = new Trie<string>(root);
Console.WriteLine($"Data structures (C# toolchain): trie size = {trie.Size}");
