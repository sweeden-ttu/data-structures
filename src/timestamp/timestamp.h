#ifndef TIMESTAMP_H
#define TIMESTAMP_H

#include <stdint.h>
#include <time.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    uint64_t seconds;
    uint64_t nanoseconds;
    char isotimestamp[64];
} Timestamp;

void timestamp_now(Timestamp* ts) {
    struct timespec spec;
    clock_gettime(CLOCK_REALTIME, &spec);
    ts->seconds = (uint64_t)spec.tv_sec;
    ts->nanoseconds = (uint64_t)spec.tv_nsec;
    
    struct tm tm_info;
    gmtime_r(&spec.tv_sec, &tm_info);
    strftime(ts->isotimestamp, sizeof(ts->isotimestamp), "%Y-%m-%dT%H:%M:%S", &tm_info);
}

uint64_t timestamp_to_unix_ms(Timestamp* ts) {
    return ts->seconds * 1000ULL + ts->nanoseconds / 1000000ULL;
}

void timestamp_to_iso8601(Timestamp* ts, char* buffer, size_t size) {
    snprintf(buffer, size, "%s.%09lluZ", ts->isotimestamp, (unsigned long long)ts->nanoseconds);
}

#ifdef __cplusplus
}
#endif

#endif
