#ifndef ENCRYPTED_NODE_H
#define ENCRYPTED_NODE_H

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    uint8_t node_id[16];
    uint8_t mac_address[6];
    double radius;
    double diameter;
    double volume;
    uint64_t timestamp;
    uint8_t encrypted;
} EncryptedNode;

void node_init(EncryptedNode* node, const char* node_id, const char* mac) {
    memset(node->node_id, 0, sizeof(node->node_id));
    memset(node->mac_address, 0, sizeof(node->mac_address));
    
    size_t id_len = strlen(node_id);
    for (size_t i = 0; i < id_len && i < 16; i++) {
        node->node_id[i] = (uint8_t)node_id[i];
    }
    
    if (mac) {
        sscanf(mac, "%hhx:%hhx:%hhx:%hhx:%hhx:%hhx",
               &node->mac_address[0], &node->mac_address[1], &node->mac_address[2],
               &node->mac_address[3], &node->mac_address[4], &node->mac_address[5]);
    }
    
    node->timestamp = (uint64_t)time(NULL);
    node->encrypted = 0;
    
    node->radius = 1.0;
    node->diameter = node->radius * 2.0;
    node->volume = (4.0 / 3.0) * M_PI * pow(node->radius, 3.0);
}

void node_set_radius(EncryptedNode* node, double r) {
    node->radius = r;
    node->diameter = r * 2.0;
    node->volume = (4.0 / 3.0) * M_PI * pow(r, 3.0);
}

void node_encrypt(EncryptedNode* node) {
    for (int i = 0; i < 16; i++) {
        node->node_id[i] ^= 0xFF;
    }
    for (int i = 0; i < 6; i++) {
        node->mac_address[i] ^= 0xFF;
    }
    node->encrypted = 1;
}

void node_decrypt(EncryptedNode* node) {
    for (int i = 0; i < 16; i++) {
        node->node_id[i] ^= 0xFF;
    }
    for (int i = 0; i < 6; i++) {
        node->mac_address[i] ^= 0xFF;
    }
    node->encrypted = 0;
}

void node_print(EncryptedNode* node) {
    printf("Node ID: ");
    for (int i = 0; i < 16 && node->node_id[i]; i++) {
        printf("%02x", node->node_id[i]);
    }
    printf("\nMAC: %02x:%02x:%02x:%02x:%02x:%02x\n",
           node->mac_address[0], node->mac_address[1], node->mac_address[2],
           node->mac_address[3], node->mac_address[4], node->mac_address[5]);
    printf("Radius: %.17g (64-bit)\n", node->radius);
    printf("Diameter: %.17g (64-bit)\n", node->diameter);
    printf("Volume: %.17g (64-bit)\n", node->volume);
    printf("Timestamp: %lu\n", node->timestamp);
    printf("Encrypted: %s\n", node->encrypted ? "yes" : "no");
}

uint64_t node_get_radius_bits(EncryptedNode* node) {
    uint64_t* ptr = (uint64_t*)&node->radius;
    return *ptr;
}

uint64_t node_get_diameter_bits(EncryptedNode* node) {
    uint64_t* ptr = (uint64_t*)&node->diameter;
    return *ptr;
}

uint64_t node_get_volume_bits(EncryptedNode* node) {
    uint64_t* ptr = (uint64_t*)&node->volume;
    return *ptr;
}

#ifdef __cplusplus
}
#endif

#endif
