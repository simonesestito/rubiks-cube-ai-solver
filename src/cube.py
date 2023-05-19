'''
Rubik's Cube simulator class.

Explained in the noteboks/cube_simulator.ipynb notebook,
with all previous stages to get to this point.
'''

import ctypes
import os
import sys

# Load the shared library containing the C functions
_lib = ctypes.CDLL(os.path.dirname(os.path.realpath(sys.argv[0])) + '/libcube.so')

# Define the return types and argument types

_cube_type = ctypes.POINTER(ctypes.c_uint32)
_faces_type = ctypes.c_uint8 * (6 * 3 * 3)

## create_cube
_lib.create_cube.restype = _cube_type
_lib.create_cube_from.argtypes = [_faces_type]
_lib.create_cube_from.restype = _cube_type

## perform_action
_lib.perform_action.argtypes = [_cube_type, ctypes.c_char_p]
_lib.get_cell.argtypes = [_cube_type, ctypes.c_uint8, ctypes.c_uint8, ctypes.c_uint8]
_lib.get_cell.restype = ctypes.c_uint8
_lib.solved_faces.argtypes = [_cube_type]
_lib.solved_faces.restype = ctypes.c_uint8

## face rotations
_lib.face0_clock.argtypes = [_cube_type]
_lib.face0_counterclock.argtypes = [_cube_type]
_lib.face1_clock.argtypes = [_cube_type]
_lib.face1_counterclock.argtypes = [_cube_type]
_lib.face2_clock.argtypes = [_cube_type]
_lib.face2_counterclock.argtypes = [_cube_type]
_lib.face3_clock.argtypes = [_cube_type]
_lib.face3_counterclock.argtypes = [_cube_type]
_lib.face4_clock.argtypes = [_cube_type]
_lib.face4_counterclock.argtypes = [_cube_type]
_lib.face5_clock.argtypes = [_cube_type]
_lib.face5_counterclock.argtypes = [_cube_type]

## solution utils
_lib.is_solved.argtypes = [_cube_type]
_lib.is_solved.restype = ctypes.c_bool
_lib.solution_percentage.argtypes = [_cube_type]
_lib.solution_percentage.restype = ctypes.c_double


class Cube:
  def __init__(self, faces=None):
    if faces is None:
      self.cube = _lib.create_cube()
    else:
      self.cube = _lib.create_cube_from(_faces_type(*[
        ctypes.c_uint8(faces[face][row][col])
        for face in range(6)
        for row in range(3)
        for col in range(3)
      ]))

  def __del__(self):
    if hasattr(self, 'cube'):
      _lib.free(self.cube)

  def perform_action(self, actions):
    if type(actions) is list:
      actions = str.join(' ', actions)

    _lib.perform_action(self.cube, ctypes.c_char_p(actions.encode('utf-8')))

  def face0_clock(self):
    _lib.face0_clock(self.cube)

  def face0_counterclock(self):
    _lib.face0_counterclock(self.cube)
  
  def face1_clock(self):
    _lib.face1_clock(self.cube)

  def face1_counterclock(self):
    _lib.face1_counterclock(self.cube)

  def face2_clock(self):
    _lib.face2_clock(self.cube)

  def face2_counterclock(self):
    _lib.face2_counterclock(self.cube)

  def face3_clock(self):
    _lib.face3_clock(self.cube)

  def face3_counterclock(self):
    _lib.face3_counterclock(self.cube)

  def face4_clock(self):
    _lib.face4_clock(self.cube)

  def face4_counterclock(self):
    _lib.face4_counterclock(self.cube)
  
  def face5_clock(self):
    _lib.face5_clock(self.cube)

  def face5_counterclock(self):
    _lib.face5_counterclock(self.cube)

  def is_solved(self):
    return _lib.is_solved(self.cube)

  def solution_percentage(self):
    return _lib.solution_percentage(self.cube)

  def get_cell(self, face, row, col):
    return _lib.get_cell(self.cube, face, row, col)

  def solved_faces(self):
    return _lib.solved_faces(self.cube)

  def _print_cell(self, face, row, col):
    return [
      '\033[42mg',
      '\033[47mw',
      '\033[101mo',
      '\033[41mr',
      '\033[43my',
      '\033[44mb',
    ][self.get_cell(face, row, col)] + ' \033[0m'

  def __repr__(self):
    return Cube.__str__(self)
  
  def __str__(self):
    cube_image = ''

    # First row = face 1
    for row in range(3):
      cube_image += ' ' * 7
      for col in range(3):
        cube_image += self._print_cell(1, row, col)
      cube_image += '\n'
    cube_image += '\n'
    
    # Second row = faces 2, 0, 3, 5
    for row in range(3):
      for face in (2, 0, 3, 5):
        for col in range(3):
          cube_image += self._print_cell(face, row, col)
        cube_image += ' '
      cube_image += '\n'
    cube_image += '\n'

    # Third row = face 4
    for row in range(3):
      cube_image += ' ' * 7
      for col in range(3):
        cube_image += self._print_cell(4, row, col)
      cube_image += '\n'

    return cube_image

  def is_same(self, faces):
    for face in range(6):
      for row in range(3):
        for col in range(3):
          if self.get_cell(face, row, col) != faces[face][row][col]:
            return False
    return True