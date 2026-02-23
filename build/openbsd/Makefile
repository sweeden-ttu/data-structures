# Makefile for OpenBSD
CC = gcc
CFLAGS = -Wall -Wextra -O2
TARGET = stack_openbsd

all: $(TARGET)

$(TARGET): ../stack_crossplatform.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)
