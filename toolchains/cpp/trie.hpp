#ifndef DATASTRUCTURES_TREE_HPP
#define DATASTRUCTURES_TREE_HPP

#include "trie_node.hpp"
#include <memory>

/** LangChain namespace: chain/trie structures */
namespace langchain {

template <typename T>
class Trie {
public:
    explicit Trie(std::unique_ptr<TrieNode<T>> root = nullptr) : root_(std::move(root)) {}
    TrieNode<T>* root() { return root_.get(); }
    bool is_empty() const { return root_ == nullptr; }
    int size() const { return root_ ? count_nodes(root_.get()) : 0; }

private:
    std::unique_ptr<TrieNode<T>> root_;
    static int count_nodes(const TrieNode<T>* node) {
        int count = 1;
        for (const auto& child : node->children)
            count += count_nodes(child.get());
        return count;
    }
};

} // namespace langchain

#endif
