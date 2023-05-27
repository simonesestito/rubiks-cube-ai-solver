import torch
import random
from cube import Cube
from cubes_dataset import CUBE_MOVES_ENCODING, CubesDataloader
from training import PYTORCH_DEVICE, model
from progressbar import progressbar

def random_cube(n_moves=8):
    cube = Cube()
    done_moves = []
    for _ in range(n_moves):
        move = random.choice(
            list(CUBE_MOVES_ENCODING.keys())
        )
        cube.perform_action(move)
        rev_move = move.upper() if move.islower() else move.lower()
        done_moves.append(rev_move)
    return cube, done_moves

def test_solution(max_moves):
    # Need to fetch the next 3 right optimal moves
    new_cube, moves = random_cube()
    cubes = [ new_cube ]
    for move in moves[::-1][:3]:
        new_cube = cubes[-1].copy()
        new_cube.perform_action(move)
        cubes.append(new_cube)

    std_cube = cubes[0].copy()
    for move in moves[::-1]:
        std_cube.perform_action(move)
    assert std_cube.is_solved()

    while not cubes[-1].is_solved() and len(cubes) <= max_moves:
        # Predict next move
        X = torch.cat([
            cube.to_tensor()
            for cube in cubes[-4:]
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
    return len(cubes)

def eval_model():
    with torch.no_grad():
        model.eval()
        # Test real world cases
        total_samples, correct_samples = 10_000, 0
        
        moves_avg = 0
        for _ in progressbar(range(total_samples)):
            solved_in = test_solution(max_moves=20)
            if solved_in <= 20:
                correct_samples += 1
                moves_avg += solved_in

        # Result
        acc = correct_samples * 100 / total_samples
        print(f'Accuracy: {acc:.4f} ({correct_samples} / {total_samples})')
        print(f'Average moves: {moves_avg / correct_samples:.4f}')

if __name__ == '__main__':
    eval_model()
