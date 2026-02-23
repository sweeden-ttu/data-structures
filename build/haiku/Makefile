# Haiku cross-compile
CC = x86_64-unknown-haiku-gcc
CFLAGS = -Wall -O2
TARGET = stack_haiku
all: $(TARGET)
$(TARGET): ../../src/stack_crossplatform.c
	$(CC) $(CFLAGS) -o $@ $<
