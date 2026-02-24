#include "trie.hpp"
#include <iostream>
#include <memory>

using namespace langchain;

int main() {
    auto root = std::make_unique<TrieNode<std::string>>("root");
    root->children.push_back(std::make_unique<TrieNode<std::string>>("a"));
    root->children.push_back(std::make_unique<TrieNode<std::string>>("b"));
    Trie<std::string> trie(std::move(root));
    std::cout << "Data structures (C++ toolchain): trie size = " << trie.size() << std::endl;
    return 0;
}
