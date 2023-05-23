# Used to compile the cube.c implementation of the cube module

CC = gcc
CPP = g++
CFLAGS = -O2 
CPPFLAGS = -O2 -fPIC --std=c++17

all: src/libcube.so src/cubes_map_gen src/libcubes_map.so src/libcubes_dataset.so

clean:
	rm -f src/libcube.so src/libcubes_map.so src/cubes_map_gen

src/libcubes_dataset.so: src/cubes_dataset.cpp src/cube.c src/cubes_map_common.cpp
	$(CPP) $(CPPFLAGS) -shared -o $@ $^

src/libcubes_map.so: src/cubes_map.cpp src/cube.c src/cubes_map_common.cpp
	$(CPP) $(CPPFLAGS) -shared -o $@ $^

src/cubes_map_gen: src/cubes_map_gen.cpp src/cube.c src/cubes_map_common.cpp
	$(CPP) $(CPPFLAGS) -o $@ $^

src/libcube.so: src/cube.c
	$(CC) $(CFLAGS) -shared -o $@ $^
