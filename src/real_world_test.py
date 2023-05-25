import torch
import random
from cube import Cube
from cubes_dataset import CUBE_MOVES_ENCODING
from training import PYTORCH_DEVICE, model
from progressbar import progressbar

moves = [ "U", "U'", "D", "D'", "L", "L'", "R", "R'", "F", "F'", "B", "B'"]


def random_cube(n_moves=8):
    cube = Cube()
    done_moves = []
    for _ in range(n_moves):
        move = random.choice(moves)
        cube.perform_action(move)
        rev_move = move[0] if move[-1] == "'" else (move + "'")
        done_moves.append(rev_move)
    return cube, moves

def test_solution(max_moves=30):
    # Need to fetch the next 3 right optimal moves
    new_cube, moves = random_cube()
    cubes = [ new_cube ]
    latest_moves = moves[-1:-4:-1]
    for move in latest_moves:
        new_cube = cubes[-1].copy()
        new_cube.perform_action(move)
        cubes.append(new_cube)

    while not cubes[-1].is_solved() and len(cubes) < max_moves:
        # Predict next move
        X = torch.cat([
            cube.to_tensor()
            for cube in cubes
        ]).to(PYTORCH_DEVICE)
        pred = model(X)
        move_i = torch.argmax(pred).item()
        move = (
            list(CUBE_MOVES_ENCODING.keys())
            [list(CUBE_MOVES_ENCODING.values()).index(move_i)]
        )
        new_cube = cubes[-1].copy()
        new_cube.perform_action(move)
        cubes.append(new_cube)
    return len(cubes) < max_moves

def eval_model():
    with torch.no_grad():
        model.eval()
        # Test real world cases
        total_samples, correct_samples = 300, 0
        
        for _ in progressbar(range(total_samples)):
            if test_solution(max_moves=100):
                correct_samples += 1

        # Result
        acc = correct_samples * 100 / total_samples
        print(f'Accuracy: {acc:.4f} ({correct_samples} / {total_samples})')

if __name__ == '__main__':
    eval_model()
