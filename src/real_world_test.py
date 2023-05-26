import torch
import random
from cube import Cube
from cubes_dataset import CUBE_MOVES_ENCODING, CubesDataloader
from training import PYTORCH_DEVICE, model
from progressbar import progressbar

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
    return cube, done_moves

def is_known(cubes_seq):
    cubes_seq = cubes_seq[-4:]
    assert not cubes_seq[-1].is_solved()
    cubes_seq = [ c.to_tensor() for c in cubes_seq ]
    cubes_seq = torch.cat(cubes_seq).reshape(4,24)
    data = CubesDataloader()
    for i in progressbar(range(len(data))):
        t = data[i][0]
        assert t.shape == cubes_seq.shape
        assert t.dtype == cubes_seq.dtype
        if torch.equal(t, cubes_seq):
            return True
    return False

def test_solution(max_moves):
    # Need to fetch the next 3 right optimal moves
    new_cube, moves = random_cube()
    cubes = [ new_cube ]
    for move in moves[::-1][:3]:
        new_cube = cubes[-1].copy()
        new_cube.perform_action(move)
        cubes.append(new_cube)

    assert is_known(cubes)

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
        print(move_i, move, moves[::-1][len(cubes)-1])
        new_cube = cubes[-1].copy()
        new_cube.perform_action(move)
        cubes.append(new_cube)

        test_cube = cubes[-2].copy()
        test_cube.perform_action(
                moves[::-1][len(cubes)-2]
        )
        print(test_cube)
        assert test_cube.is_solved()
    print()
    return len(cubes) <= max_moves

def eval_model():
    with torch.no_grad():
        model.eval()
        # Test real world cases
        total_samples, correct_samples = 100, 0
        
        for _ in range(total_samples):#progressbar(range(total_samples)):
            if test_solution(max_moves=4):
                correct_samples += 1

        # Result
        acc = correct_samples * 100 / total_samples
        print(f'Accuracy: {acc:.4f} ({correct_samples} / {total_samples})')

if __name__ == '__main__':
    eval_model()
