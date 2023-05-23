'''
Rubik's Cube List Dataset of solved cubes.
'''

import ctypes
from cube import Cube
import os
import numpy as np

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

    return cube_samples['cube'], cube_samples['move']