# Data type namespace assignment: LangGraph, LangFlow, LangChain, ScottWeedenLang

All data type structures in Swift, Objective-C, C++, C#, Java, and TypeScript belong to one of these four concrete namespaces.

## LangChain (chain / trie / trie structures)

| Language    | Types |
|------------|--------|
| **Java**   | `langchain.Trie`, `langchain.TrieNode`, `langchain.BinaryTrieNode` |
| **C#**     | `LangChain.Trie`, `LangChain.TrieNode` (toolchains) |
| **C++**    | `langchain::Trie`, `langchain::TrieNode` |
| **TypeScript** | (chain/trie types if added; currently graph-only in this repo) |
| **Swift**  | (toolchain trie/trie types if added) |
| **Objective-C** | (toolchain trie/trie types if added) |

## LangGraph (graph structures and graph filter agents)

| Language    | Types |
|------------|--------|
| **Java**   | `langgraph.BloomingDirectedGraphFilterAgents`, `langgraph.Collection`, `langgraph.Collection.Node` |
| **C#**     | `LangGraph.BloomingDirectedGraphFilterAgents`, `LangGraph.Collection`, `LangGraph.Collection.Node` |
| **TypeScript** | `LangGraph.BloomingDirectedGraph`, `LangGraph.Node`, `LangGraph.Edge` (and `LangGraph` namespace export) |
| **Swift**  | `BloomingDirectedGraphFilterAgents`, `Node` (filter collection; namespace comment) |
| **Objective-C** | `BDGNode`, `BloomingDirectedGraphFilterAgents` (namespace comment: LangGraph) |

## LangFlow (flow / trie root / trigger process agent)

| Language    | Types |
|------------|--------|
| **Java**   | `langflow.BloomingDirectedGraphTriggerProcessAgent`, `langflow.TriggerProcessAgent`, `langflow.TrieOfBloomingDirectedGraphsWithAgentsAndFilters` (Trie root in `langflow.Root`) |
| **C#**     | `LangFlow.TriggerProcessAgent`, `LangFlow.TrieOfBloomingDirectedGraphsWithAgentsAndFilters`, `LangFlow.TrieNodeValue` |
| **TypeScript** | Trie root, trigger agent (namespace comment: LangFlow) |
| **Swift**  | `TrieOfBloomingDirectedGraphsWithAgentsAndFilters`, `TrieNodeValue`, `TriggerNode`, `BloomingDirectedGraphTriggerProcessAgent`; `LangFlow.TrieRoot`, `LangFlow.TrieNodeValueType` typealiases |
| **Objective-C** | Trie root (`TrieOfBloomingDirectedGraphsWithAgentsAndFilters`, `TrieNodeValue`), `BloomingDirectedGraphTriggerProcessAgent` (namespace comment: LangFlow) |

## ScottWeedenLang (entry point / utility)

| Language    | Types |
|------------|--------|
| **Java**   | `scottweedenlang.Main` |
| **C#**     | (Program entry; no explicit namespace – uses LangChain types) |
| **C++**    | `main()` (comment: ScottWeedenLang entry point) |
| **TypeScript** | `main()` (comment: ScottWeedenLang entry point) |

## Summary

- **LangChain**: Trie, TrieNode, BinaryTrieNode, Trie, TrieNode (chain/trie/trie data structures).
- **LangGraph**: BloomingDirectedGraph, Node, Edge, BloomingDirectedGraphFilterAgents, Collection (graph and graph filter agents).
- **LangFlow**: Trie root anchor, TriggerProcessAgent, BloomingDirectedGraphTriggerProcessAgent, TrieNodeValue (flow and trigger).
- **ScottWeedenLang**: Main, Program, main() (entry points and utilities).
