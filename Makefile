# Used to compile the cube.c implementation of the cube module

CC = gcc
CPP = g++
CFLAGS = -O2 -fPIC

all: src/libcube.so src/cubes_map_gen src/libcubes_map.so

clean:
	rm -f src/cube.so src/cubes_map.so src/cubes_map_gen

src/libcubes_map.so: src/cubes_map.cpp src/cube.c src/cubes_map_common.cpp
	$(CPP) $(CFLAGS) -shared -o $@ $^

src/cubes_map_gen: src/cubes_map_gen.cpp src/cube.c src/cubes_map_common.cpp
	$(CPP) $(CFLAGS) -o $@ $^

src/libcube.so: src/cube.c
	$(CC) $(CFLAGS) -shared -o $@ $^