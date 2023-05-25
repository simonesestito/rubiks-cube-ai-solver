'''
Rubik's Cube List Dataset of solved cubes.
'''

import ctypes
import os
import torch
import torch.utils.data

CUBES_MAP_FILE = os.getenv('CUBES_MAP_FILE', 'cubes_map.bin')

cubes_size = 8-5

class CubeSample(ctypes.Structure):
    _fields_ = [
        ("cube", ctypes.c_uint8 * 2 * 2 * 6 * cubes_size),
        ("move", ctypes.c_char)
    ]

# Load the shared library containing the C functions
_lib = ctypes.CDLL(os.path.dirname(os.path.realpath(__file__)) + '/libcubes_dataset.so')

_lib.read_cube.restype = ctypes.c_int
_lib.read_cube.argtypes = [
    ctypes.POINTER(CubeSample), # cube_sample
    ctypes.c_char_p,            # filename
    ctypes.c_size_t,            # sample_no
]

_lib.get_cubes_len.restype = ctypes.c_size_t
_lib.get_cubes_len.argtypes = [
    ctypes.c_char_p,            # filename
]

class CubesDataloader(torch.utils.data.Dataset):
    def __init__(self, filename = CUBES_MAP_FILE):
        self.filename = filename
    
    def __len__(self):
        total_len = _lib.get_cubes_len(ctypes.c_char_p(self.filename.encode('ascii')))
        print('[pytorch] Dataset length:', total_len)
        return total_len
    
    def __getitem__(self, idx):
        cube_sample = CubeSample()
        success = _lib.read_cube(ctypes.byref(cube_sample), ctypes.c_char_p(self.filename.encode('ascii')), ctypes.c_size_t(idx))
        if not success:
            return None
        cubes_arr = cube_sample.cube
        return torch.reshape(torch.Tensor(cubes_arr), (cubes_size,24)), CUBE_MOVES_ENCODING[cube_sample.move.decode('ascii')]

CUBE_MOVES_ENCODING = {
    'U': 0,
    'u': 1,
    'D': 2,
    'd': 3,
    'L': 4,
    'l': 5,
    'R': 6,
    'r': 7,
    'F': 8,
    'f': 9,
    'B': 10,
    'b': 11,
    # Also, remove the solved cube from the dataset
}
