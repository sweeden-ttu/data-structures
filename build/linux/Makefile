# Native Linux build
CC = gcc
CFLAGS = -Wall -Wextra -O2
TARGET = stack_linux
all: $(TARGET)
$(TARGET): ../../src/stack_crossplatform.c
	$(CC) $(CFLAGS) -o $@ $<
