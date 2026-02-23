# Makefile for OS/2
# Requires OpenWatcom or EMX

CC = wcl
CFLAGS = -bt=os2 -q
TARGET = stack_os2.exe

all: $(TARGET)

$(TARGET): stack_crossplatform.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)
