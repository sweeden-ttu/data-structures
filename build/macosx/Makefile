# Makefile for Mac OS X (cross-compile from Linux)
# Requires Apple SDK or osx-cross-toolchain

CC = x86_64-apple-darwin14-clang
CFLAGS = -Wall -O2
TARGET = stack_macos

all: $(TARGET)

$(TARGET): ../stack_crossplatform.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)
