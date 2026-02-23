#include <stdio.h>
#include "timestamp/timestamp.h"
#include "encrypted_node/encrypted_node.h"

int main() {
    Timestamp ts;
    timestamp_now(&ts);
    
    char iso[128];
    timestamp_to_iso8601(&ts, iso, sizeof(iso));
    printf("Timestamp: %s\n", iso);
    printf("Unix ms: %lu\n", timestamp_to_unix_ms(&ts));
    
    EncryptedNode node;
    node_init(&node, "C2", "e4:b9:7a:f8:95:1b");
    
    printf("\nNode with radius=1.0:\n");
    node_print(&node);
    printf("Radius bits: %016lx\n", node_get_radius_bits(&node));
    
    node_set_radius(&node, 3.14159);
    
    printf("\nNode with radius=3.14159:\n");
    node_print(&node);
    printf("Radius bits: %016lx\n", node_get_radius_bits(&node));
    
    return 0;
}
