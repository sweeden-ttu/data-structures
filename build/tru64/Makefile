# Makefile for Tru64 UNIX (formerly Digital UNIX, DEC OSF/1)
# Requires Tru64 C compiler (cc) or GCC

CC = cc
CFLAGS = -std=c99 -Wall -O2
TARGET = stack_tru64

all: $(TARGET)

$(TARGET): ../../src/stack_crossplatform.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)
