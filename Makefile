# Used to compile the cube.c implementation of the cube module

CC = gcc
CFLAGS = -shared -O2

src/cube.so: src/cube.c
	$(CC) $(CFLAGS) -o $@ $^