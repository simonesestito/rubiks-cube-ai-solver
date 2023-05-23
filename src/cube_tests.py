import pytest
import random
import os
from cube import Cube
from cubes_map import CubesMap
from main import load_cube_faces
import cubes_dataset

RANDOM_TEST_REPS = 1000

moves = [ "U", "U'", "D", "D'", "L", "L'", "R", "R'", "F", "F'", "B", "B'"]
assert len(moves) == 12

if 'known_cubes' not in globals():
    cubes_map = None #CubesMap()

'''
Return 2 cubes so that we can work on one and compare it to the other.
'''
def randomize_cube(n_moves = 20):
    cube1, cube2 = Cube(), Cube()
    for _ in range(n_moves):
        move = random.choice(moves)
        cube1.perform_action(move)
        cube2.perform_action(move)
    return cube1, cube2

def _test_reverse_move(move):
    for _ in range(RANDOM_TEST_REPS):
        cube, original = randomize_cube()
        cube.perform_action(move)

        # Reverse the move
        if move.endswith("'"):
            cube.perform_action(move[0])
        else:
            cube.perform_action(move + "'")

        assert cube == original, move

def _test_four_moves(move):
    for _ in range(RANDOM_TEST_REPS):
        cube, original = randomize_cube()
        for _ in range(4):
            cube.perform_action(move)
        
        assert cube == original, move

def test_cubes_map():
    for _ in range(RANDOM_TEST_REPS):
        n_moves = 8
        cube, _ = randomize_cube(n_moves=n_moves)

        for _ in range(n_moves):
            next_move = cubes_map[cube]
            assert next_move is not None
            cube.perform_action(next_move)
            if cube.is_solved():
                break
    
        assert cube.is_solved()

def test_cubes_list():
    for i in range(10):
        # Load some batches
        X, y = cubes_dataset.load_cubes_dataset_as_cubes(i, limit_batches=10)
        assert len(X) == len(y)

        for _ in range(100):
            # Choose a random cube
            j = random.randint(0, len(X) - 1)
            x, yy = X[j], y[j]
            # Check if the move to make is the same as in the map
            assert cubes_map[x] == yy, f'Map {cubes_map[x]} - list {yy}\n'+str(x)


def _test_cube(cube_faces, moves):
  cube = Cube(cube_faces)

  for move in moves.split():
    cube.perform_action(move)

  assert cube.is_solved()

def test_reverse_u():
    _test_reverse_move("U")

def test_reverse_d():
    _test_reverse_move("D")

def test_reverse_l():
    _test_reverse_move("L")

def test_reverse_r():
    _test_reverse_move("R")

def test_reverse_f():
    _test_reverse_move("F")

def test_reverse_b():
    _test_reverse_move("B")

def test_reverse_u_prime():
    _test_reverse_move("U'")

def test_reverse_d_prime():
    _test_reverse_move("D'")

def test_reverse_l_prime():
    _test_reverse_move("L'")

def test_reverse_r_prime():
    _test_reverse_move("R'")

def test_reverse_f_prime():
    _test_reverse_move("F'")

def test_reverse_b_prime():
    _test_reverse_move("B'")

def test_four_u():
    _test_four_moves("U")

def test_four_d():
    _test_four_moves("D")

def test_four_l():
    _test_four_moves("L")

def test_four_r():
    _test_four_moves("R")

def test_four_f():
    _test_four_moves("F")

def test_four_b():
    _test_four_moves("B")

def test_four_u_prime():
    _test_four_moves("U'")

def test_four_d_prime():
    _test_four_moves("D'")

def test_four_l_prime():
    _test_four_moves("L'")

def test_four_r_prime():
    _test_four_moves("R'")

def test_four_f_prime():
    _test_four_moves("F'")

def test_four_b_prime():
    _test_four_moves("B'")

def test_cube_random_1():
    # Real cubes with moves known to be correct
    # https://rubikscu.be/solver/?cube=0234426412651332611336514511343152355645366125452246462
    g, w, o, r, y, b = 0, 1, 2, 3, 4, 5
    _test_cube([
        # All faces, in order
        [[g, g, y],
        [b, w, r],
        [b, w, w]],
        [[o, g, r],
        [r, o, y],
        [r, w, o]],
        [[y, b, w],
        [g, g, o],
        [y, w, w]],
        [[g, r, g],
        [w, b, o],
        [g, b, b]],
        [[r, b, o],
        [o, r, y],
        [r, y, o]],
        [[y, r, b],
        [g, y, y],
        [w, o, b]],
    ], "U R' U F U' D D R R B B D' F' L' F' U F F B B U U F F B B L L B B")

def test_cube_random_2():
    # Real cubes with moves known to be correct
    # https://rubikscu.be/solver/?cube=0511163653245344114424533652124621142556254325363316266
    g, w, o, r, y, b = 0, 1, 2, 3, 4, 5
    _test_cube([
        [[r,o,r],
        [b,g,g],
        [y,b,o]],
        [[b,w,w],
        [w,y,g],
        [y,b,g]],
        [[o,r,b],
        [g,r,r],
        [w,w,r]],
        [[w,o,r],
        [y,o,w],
        [w,r,o]],
        [[g,y,g],
        [g,w,y],
        [o,y,y]],
        [[b,b,y],
        [o,b,r],
        [g,o,b]],
    ], "U F' L' F' R R U' F' U' D' B R R B' U B B U U R R D D R R F F U")

g, w, o, r, y, b = 0, 1, 2, 3, 4, 5
CUBE_0 = Cube([
        [[y, o, r],
         [r, g, w],
         [w, g, o]],
        [[w, b, b],
         [y, w, g],
         [g, r, y]],
        [[g, w, r],
         [o, o, r],
         [o, g, w]],
        [[r, y, g],
         [g, r, o],
         [b, y, o]],
        [[b, w, g],
         [b, y, w],
         [r, y, o]],
        [[w, r, y],
         [b, b, b],
         [y, o, b]],
    ])

def test_color_detection_cube_0():
    rootCube = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", "assets", "images", "cube-0")
    assert load_cube_faces([
        os.path.join(rootCube, 'face0.jpg'),
        os.path.join(rootCube, 'face1.jpg'),
        os.path.join(rootCube, 'face2.jpg'),
        os.path.join(rootCube, 'face3.jpg'),
        os.path.join(rootCube, 'face4.jpg'),
        os.path.join(rootCube, 'face5.jpg'),
    ]) == CUBE_0

def test_color_shuffle_cube_0():
    rootCube = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", "assets", "images", "cube-0")
    cube_faces_img = [
        os.path.join(rootCube, 'face0.jpg'),
        os.path.join(rootCube, 'face1.jpg'),
        os.path.join(rootCube, 'face2.jpg'),
        os.path.join(rootCube, 'face3.jpg'),
        os.path.join(rootCube, 'face4.jpg'),
        os.path.join(rootCube, 'face5.jpg'),
    ]

    for _ in range(10):
        random.shuffle(cube_faces_img)
        assert load_cube_faces(cube_faces_img) == CUBE_0

CUBE_1 = Cube([
    [[b, o, b],
     [y, g, b],
     [g, r, r]],
    [[b, y, y],
     [w, w, w],
     [o, g, o]],
    [[r, r, w],
     [b, o, b],
     [y, o, w]],
    [[y, o, r],
     [r, r, r],
     [g, g, y]],
    [[o, g, w],
     [y, y, w],
     [r, b, g]],
    [[g, g, w],
     [y, b, w],
     [o, o, b]],
])

def test_color_detection_cube_1():
    rootCube = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", "assets", "images", "cube-1")
    assert load_cube_faces([
        os.path.join(rootCube, 'face0.jpg'),
        os.path.join(rootCube, 'face1.jpg'),
        os.path.join(rootCube, 'face2.jpg'),
        os.path.join(rootCube, 'face3.jpg'),
        os.path.join(rootCube, 'face4.jpg'),
        os.path.join(rootCube, 'face5.jpg'),
    ]) == CUBE_1

def test_color_shuffle_cube_1():
    rootCube = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", "assets", "images", "cube-1")
    cube_faces_img = [
        os.path.join(rootCube, 'face0.jpg'),
        os.path.join(rootCube, 'face1.jpg'),
        os.path.join(rootCube, 'face2.jpg'),
        os.path.join(rootCube, 'face3.jpg'),
        os.path.join(rootCube, 'face4.jpg'),
        os.path.join(rootCube, 'face5.jpg'),
    ]

    for _ in range(10):
        random.shuffle(cube_faces_img)
        assert load_cube_faces(cube_faces_img) == CUBE_1