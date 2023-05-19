'''
Rubik's Cube map of solved cubes.
'''

import ctypes
from cube import Cube, _cube_type
import os
import sys

# Load the shared library containing the C functions
_lib = ctypes.CDLL(os.path.dirname(os.path.realpath(sys.argv[0])) + '/libcubes_map.so')

# Define the return types and argument types
_cube_map_type = ctypes.c_void_p
_string_type = ctypes.c_char_p

## load_cubes_map
_lib.load_cubes_map.restype = _cube_map_type
_lib.load_cubes_map.argtypes = [_string_type]

## get_cube_from_map
_lib.get_cube_from_map.restype = ctypes.c_char
_lib.get_cube_from_map.argtypes = [_cube_map_type, _cube_type]

## free_cubes_map
_lib.free_cubes_map.restype = None
_lib.free_cubes_map.argtypes = [_cube_map_type]


class CubesMap:
    def __init__(self, filename = 'cubes_map.bin'):
        self.cube_map = _lib.load_cubes_map(filename.encode('ascii'))

    def __del__(self):
        if hasattr(self, 'cube_map'):
            _lib.free_cubes_map(self.cube_map)
    
    def __getitem__(self, cube: Cube):
        next_move_to_make = _lib.get_cube_from_map(self.cube_map, cube.cube)
        if next_move_to_make == ' ':
            return None
        else:
            return next_move_to_make

if __name__ == '__main__':
    cubes_map = CubesMap()
    cube = Cube()
    print(cubes_map[cube])
    cube.perform_action('F')
    print(cubes_map[cube])