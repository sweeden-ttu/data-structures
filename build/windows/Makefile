# Makefile for Windows (mingw-w64)
# Install: sudo apt-get install mingw-w64

CC = x86_64-w64-mingw32-gcc
CFLAGS = -Wall -Wextra -O2
TARGET = stack_windows.exe

all: $(TARGET)

$(TARGET): ../stack_crossplatform.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)
