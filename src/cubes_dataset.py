'''
Rubik's Cube List Dataset of solved cubes.
'''

import ctypes
from cube import Cube
import os
import numpy as np
import torch

class CubeSample(ctypes.Structure):
    _fields_ = [
        ("cube", ctypes.c_uint8 * 3 * 3 * 6),
        ("move", ctypes.c_char)
    ]

# Load the shared library containing the C functions
_lib = ctypes.CDLL(os.path.dirname(os.path.realpath(__file__)) + '/libcubes_dataset.so')

_lib.read_cubes_list.restype = ctypes.c_size_t
_lib.read_cubes_list.argtypes = [
    ctypes.POINTER(CubeSample), # cube_samples
    ctypes.c_char_p,            # filename
    ctypes.c_int,               # batch_no
    ctypes.c_int,               # limit_batches
]

def load_cubes_dataset(batch_no, limit_batches = 1, filename = 'cubes_map_3.bin'):
    # Allocate cube samples
    cube_samples = np.empty(2621 * limit_batches, dtype=CubeSample)
    cubes_no = _lib.read_cubes_list(
        ctypes.cast(cube_samples.ctypes.data, ctypes.POINTER(CubeSample)),
        ctypes.c_char_p(filename.encode('ascii')),
        ctypes.c_int(batch_no),
        ctypes.c_int(limit_batches),
    )
    cube_samples = cube_samples[:cubes_no]

    return cube_samples['cube'], np.char.decode(cube_samples['move'], 'ascii')

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
    ' ': 12,
}

def load_cubes_dataset_as_tensor(batch_no, limit_batches = 1, filename = 'cubes_map_3.bin'):
    X, y = load_cubes_dataset(batch_no, limit_batches, filename)

    # Make X a tensor
    X = torch.from_numpy(X).to(torch.float32)

    # Convert y to a tensor, using index-based encoding
    y = torch.tensor([
        CUBE_MOVES_ENCODING[move]
        for move in y
    ])

    return X, y

def load_cubes_dataset_as_cubes(batch_no, limit_batches = 1, filename = 'cubes_map_3.bin'):
    X, y = load_cubes_dataset(batch_no, limit_batches, filename)

    # Make every X a cube
    X = [
        Cube(x)
        for x in X
    ]

    return X, y
