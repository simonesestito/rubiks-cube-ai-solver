'''
Rubik's Cube map of solved cubes.
'''

import ctypes
from cube import Cube, _cube_type
import os

# Load the shared library containing the C functions
_lib = ctypes.CDLL(os.path.dirname(os.path.realpath(__file__)) + '/libcubes_map.so')

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

## load_cubes_as_list
_lib.load_cubes_as_list.restype = ctypes.c_char_p
_lib.load_cubes_as_list.argtypes = [
    _string_type, # filename
    ctypes.c_size_t, # from_offset
    ctypes.c_size_t, # limit_chunks
]

class CubesMap:
    def __init__(self, filename = 'cubes_map.bin'):
        assert os.path.isfile(filename), 'Cubes map file not found'
        self.cube_map = _lib.load_cubes_map(filename.encode('ascii'))

    def __del__(self):
        if hasattr(self, 'cube_map'):
            _lib.free_cubes_map(self.cube_map)
    
    def __getitem__(self, cube: Cube):
        next_move_to_make = _lib.get_cube_from_map(self.cube_map, cube.cube).decode('ascii')
        if next_move_to_make == '-':
            return None
        else:
            return next_move_to_make

def load_cubes_as_list(filename = 'cubes_map.bin', from_offset = 0, limit_chunks = 0):
    raw_cubes_string = (ctypes.c_char * (55 * 2621 * limit_chunks))()
    _lib.load_cubes_as_list(filename.encode('ascii'), from_offset, limit_chunks, raw_cubes_string)
    assert len(raw_cubes_string) % 55 == 0, 'Invalid cubes map file'

    # Each 55 bytes there is a cube
    cubes_list = [
        (
            Cube([
                [
                    [
                        ord(raw_cubes_string[cube * 55 + face * 9 + i * 3 + j])
                        for j in range(3)
                    ]
                    for i in range(3)
                ]
                for face in range(6)
            ]),
            raw_cubes_string[cube * 55 + 54].decode('ascii'), # Move
        )
        for cube in range(len(raw_cubes_string) // 55)
    ]

    return cubes_list

if __name__ == '__main__':
    cubes_list = load_cubes_as_list(from_offset=0, limit_chunks=10)
    print(cubes_list)