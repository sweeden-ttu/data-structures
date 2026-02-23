#include <stdlib.h>

typedef struct {
    void** items;
    size_t size;
    size_t capacity;
} Stack;

Stack* stack_new(size_t capacity) {
    Stack* s = malloc(sizeof(Stack));
    s->items = malloc(sizeof(void*) * capacity);
    s->size = 0;
    s->capacity = capacity;
    return s;
}

void stack_push(Stack* s, void* item) {
    if (s->size >= s->capacity) {
        s->capacity *= 2;
        s->items = realloc(s->items, sizeof(void*) * s->capacity);
    }
    s->items[s->size++] = item;
}

void* stack_pop(Stack* s) {
    return s->size ? s->items[--s->size] : NULL;
}

void stack_free(Stack* s) {
    free(s->items);
    free(s);
}
