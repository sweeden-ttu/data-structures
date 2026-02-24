// blooming_directed_graph_trigger_process_agent – Objective-C. Namespace: LangFlow.
#import "Collection.h"

NS_ASSUME_NONNULL_BEGIN

@interface BloomingDirectedGraphTriggerProcessAgent : NSObject
+ (NSDictionary *)triggerWithNode:(BDGNode *)node action:(NSString *)action payload:(NSDictionary *)payload;
@end

NS_ASSUME_NONNULL_END
