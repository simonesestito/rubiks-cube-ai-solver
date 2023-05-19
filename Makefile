# Used to compile the cube.c implementation of the cube module

CC = gcc
CPP = g++
CFLAGS = -O2

all: src/cube.so src/cubes_map_gen

clean:
	rm -f src/cube.so src/cube.o src/cubes_map_gen

src/cubes_map_gen: src/cubes_map_gen.cpp src/cube.c
	$(CPP) $(CFLAGS) -o $@ $^

src/cube.so: src/cube.o
	$(CC) $(CFLAGS) -shared -o $@ $^

src/cube.o: src/cube.c
	$(CC) $(CFLAGS) -c -o $@ $^