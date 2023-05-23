from cubes_map import CubesMap
from cube import Cube
from cubes_dataset import CUBE_MOVES_ENCODING
import random
from progressbar import progressbar
from training import model, PYTORCH_DEVICE
import torch.nn as nn

if 'known_cubes' not in globals():
  known_cubes = CubesMap(filename = './cubes_map.bin')
else:
  print('Cubes map already loaded')

moves = [*CUBE_MOVES_ENCODING.keys()][:-1]

def randomize_cube(n_moves = 8):
    cube = Cube()
    for _ in range(n_moves):
        move = random.choice(moves)
        cube.perform_action(move)
    return cube

if __name__ == '__main__':
    total_cubes = 0
    correct_cubes = 0

    for _ in progressbar(range(100_000)):
        cube = randomize_cube()

        next_move = random.choice(moves)
        cube.perform_action(next_move)

        if known_cubes[cube] is None:
            total_cubes += 1
            prediction = model(cube.to_tensor().to(PYTORCH_DEVICE))
            y = nn.Softmax(dim=1)(prediction).argmax(1)
            if y == CUBE_MOVES_ENCODING[next_move]:
                correct_cubes += 1
            else:
                print(y, end=' ')
    
    print(f'Accuracy: {correct_cubes / total_cubes * 100:.4f}%')
