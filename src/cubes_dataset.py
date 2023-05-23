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

_lib.read_cubes_list.restype = None
_lib.read_cubes_list.argtypes = [
    ctypes.POINTER(CubeSample), # cube_samples
    ctypes.c_char_p,            # filename
    ctypes.c_int,               # batch_no
    ctypes.c_int,               # limit_batches
]

def load_cubes_dataset(batch_no, limit_batches = 1, filename = 'cubes_map.bin'):
    # Allocate cube samples
    cube_samples = np.empty(2621 * limit_batches, dtype=CubeSample)
    _lib.read_cubes_list(
        ctypes.cast(cube_samples.ctypes.data, ctypes.POINTER(CubeSample)),
        ctypes.c_char_p(filename.encode('ascii')),
        ctypes.c_int(batch_no),
        ctypes.c_int(limit_batches),
    )

    return cube_samples['cube'], np.char.decode(cube_samples['move'], 'ascii')

def load_cubes_dataset_as_tensor(batch_no, limit_batches = 1, filename = 'cubes_map.bin'):
    X, y = load_cubes_dataset(batch_no, limit_batches, filename)

    # Make X a tensor
    X = torch.from_numpy(X.reshape())

    # Flat the X
    X = torch.flatten(X)

    return X, y

def load_cubes_dataset_as_cubes(batch_no, limit_batches = 1, filename = 'cubes_map.bin'):
    X, y = load_cubes_dataset(batch_no, limit_batches, filename)

    # Make every X a cube
    X = [
        Cube(x)
        for x in X
    ]

    return X, y
