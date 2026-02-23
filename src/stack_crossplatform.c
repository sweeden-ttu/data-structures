/*
 * Data Structures - Stack Implementation
 * Cross-platform compatible C code
 */

#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
    #include <malloc.h>
#endif

typedef struct Stack {
    void** items;
    size_t size;
    size_t capacity;
} Stack;

Stack* stack_create(size_t capacity) {
    Stack* s = (Stack*)malloc(sizeof(Stack));
    if (!s) return NULL;
    
    s->items = (void**)malloc(sizeof(void*) * capacity);
    if (!s->items) {
        free(s);
        return NULL;
    }
    
    s->size = 0;
    s->capacity = capacity;
    return s;
}

int stack_push(Stack* s, void* item) {
    if (!s || !item) return -1;
    
    if (s->size >= s->capacity) {
        size_t new_cap = s->capacity * 2;
        void** new_items = (void**)realloc(s->items, sizeof(void*) * new_cap);
        if (!new_items) return -1;
        s->items = new_items;
        s->capacity = new_cap;
    }
    
    s->items[s->size++] = item;
    return 0;
}

void* stack_pop(Stack* s) {
    if (!s || s->size == 0) return NULL;
    return s->items[--s->size];
}

void* stack_peek(Stack* s) {
    if (!s || s->size == 0) return NULL;
    return s->items[s->size - 1];
}

size_t stack_size(Stack* s) {
    return s ? s->size : 0;
}

int stack_is_empty(Stack* s) {
    return s ? (s->size == 0) : 1;
}

void stack_clear(Stack* s) {
    if (s) s->size = 0;
}

void stack_destroy(Stack* s) {
    if (s) {
        free(s->items);
        free(s);
    }
}

#ifndef STACK_LIB
#include <stdio.h>
int main() {
    printf("Stack Data Structure - Cross-Platform Build\n");
    printf("==========================================\n\n");
    
    Stack* s = stack_create(4);
    
    stack_push(s, "first");
    stack_push(s, "second");
    stack_push(s, "third");
    
    printf("Pushed 3 items\n");
    printf("Size: %zu\n", stack_size(s));
    printf("Peek: %s\n", (char*)stack_peek(s));
    printf("Pop: %s\n", (char*)stack_pop(s));
    printf("Pop: %s\n", (char*)stack_pop(s));
    printf("Remaining: %zu\n", stack_size(s));
    
    stack_destroy(s);
    printf("\nStack destroyed - Success!\n");
    return 0;
}
#endif
