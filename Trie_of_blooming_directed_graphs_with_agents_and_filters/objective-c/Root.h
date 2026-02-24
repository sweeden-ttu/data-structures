// Root anchor: Trie_of_blooming_directed_graphs_with_agents_and_filters
// Namespace: LangFlow (flow/trie/root anchor).
// IEEE 752 64-bit geometrica Z field (zed): see docs/IEEE_752_64BIT_GEOMETRICA_Z_FIELD_ZED_SPECIFICATIONS.md

#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN

@interface TrieNodeValue : NSObject
@property (nonatomic, nullable) id graphRef;
@property (nonatomic, nullable) id filterAgentsRef;
@property (nonatomic, nullable) id triggerProcessAgentRef;
@end

@interface TrieOfBloomingDirectedGraphsWithAgentsAndFilters : NSObject
- (void)insertKey:(NSString *)key value:(TrieNodeValue *)value;
- (nullable TrieNodeValue *)get:(NSString *)key;
- (BOOL)startsWithPrefix:(NSString *)prefix;
@end

/// Global root anchor (Trie_of_blooming_directed_graphs_with_agents_and_filters).
FOUNDATION_EXPORT TrieOfBloomingDirectedGraphsWithAgentsAndFilters *Trie_of_blooming_directed_graphs_with_agents_and_filters(void);

NS_ASSUME_NONNULL_END
