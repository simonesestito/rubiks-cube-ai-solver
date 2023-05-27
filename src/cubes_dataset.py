'''
Rubik's Cube List Dataset of solved cubes.
'''

import ctypes
import os
import torch
import torch.utils.data
from cube import Cube

CUBES_MAP_FILE = os.getenv('CUBES_MAP_FILE', 'cubes_map.bin')

cubes_size = 8-4

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
    def __init__(self, filename = CUBES_MAP_FILE, cast = 'tensor'):
        self.filename = filename
        self.cast = cast
    
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
        if self.cast == 'tensor':
            return torch.reshape(torch.Tensor(cubes_arr), (cubes_size,24)), CUBE_MOVES_ENCODING[cube_sample.move.decode('ascii')]
        elif self.cast == 'cube':
            return [
                    Cube(c) for c in cubes_arr
            ], cube_sample.move.decode('ascii')
        else:
            return cubes_arr, cube_sample.move.decode('ascii')

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

if __name__ == '__main__':
    from progressbar import progressbar
    import random

    def random_cube(n_moves=4):
        cube = Cube()
        done_moves = []
        for _ in range(n_moves):
            move = random.choice(
                list(CUBE_MOVES_ENCODING.keys())
            )
            cube.perform_action(move)
            rev_move = move.upper() if move.islower() else move.lower()
            done_moves.append(rev_move)

        cc = cube.copy()
        for move in done_moves[::-1]:
            cc.perform_action(move)
        assert cc.is_solved()
        return cube, done_moves

    def find_cubes(cubes_seq, move):
        print(move)
        exp = cubes_seq[-1].copy()
        exp.perform_action(move)

        assert not cubes_seq[-1].is_solved()
        assert not exp.is_solved()

        for i in progressbar(range(len(dataset))):
            cc, m = dataset[i]
            assert len(cc) == 4
            b, c, d, e = cc
            if b == cubes_seq[1] and c == cubes_seq[2] and d == cubes_seq[3]:
                if e != exp:
                    print('\nE (from dataset)\n', e, sep='')
                    print('\n\nExp\n', exp, sep='')
                assert e == exp
                return [b, c, d, e], m
        else:
            print('\n\nExp\n', exp, sep='')
            assert False

    # Test!
    dataset = CubesDataloader(cast='cube')
    # cube, moves = random_cube(n_moves=5)
    # a, b, c, d = None, None, None, cube
    # for m in moves[::-1][:3]:
    #     e = d.copy()
    #     e.perform_action(m)
    #     print('Move ', m ,'\n', e, sep='')
    #     a, b, c, d = b, c, d, e
    # # Assert it can be found
    # _, new_move = find_cubes([a,b,c,d], moves[::-1][3])
    # assert new_move == moves[::-1][4], f'{new_move} != {moves[::-1][4]}'
    # print('\n\n=================\n\n')

    # Take a cubes_seq [A,B,C,D]
    cubes_seq, move = dataset[200]
    assert len(cubes_seq) == 4
    # Check if there is a sequence with [B,C,D,_]
    e = cubes_seq[-1].copy()
    e.perform_action(move)
    assert not e.is_solved()

    a, b, c, d = cubes_seq
    print('\n', a, sep='')
    print('\n', b, sep='')
    print('\n', c, sep='')
    while not d.is_solved():
        print('\n', d, sep='')
        (a, b, c, d), move = find_cubes([a,b,c,d], move)
        e = d.copy()
        e.perform_action(move)
        if e.is_solved():
            print('\n', e, sep='')
            break



