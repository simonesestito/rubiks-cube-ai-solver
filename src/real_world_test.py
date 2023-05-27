import torch
import random
from cube import Cube
from cubes_dataset import CUBE_MOVES_ENCODING
from training import PYTORCH_DEVICE, model
from progressbar import progressbar
import matplotlib.pyplot as plt

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

def test_solution(max_moves, n_moves):
    # Need to fetch the next 3 right optimal moves
    new_cube, moves = random_cube(n_moves=n_moves)
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

def eval_model(n_moves):
    with torch.no_grad():
        model.eval()
        # Test real world cases
        total_samples, correct_samples = 10_000, 0
        
        moves_avg = 0
        for _ in progressbar(range(total_samples)):
            solved_in = test_solution(max_moves=n_moves*5, n_moves=n_moves)
            if solved_in <= 20:
                correct_samples += 1
                moves_avg += solved_in

        # Result
        moves_avg /= correct_samples
        acc = correct_samples * 100 / total_samples

        return acc, moves_avg

if __name__ == '__main__':
    success_rates, moves_avgs = [], []
    for i in range(5, 13):
        success_rate, moves_avg = eval_model(n_moves=i)
        success_rates.append(success_rate)
        moves_avgs.append(moves_avg)
    
    # Plot
    plt.grid(True, linewidth=0.5, color='#555555', linestyle='-')
    plt.plot(range(5, 13), success_rates, label='Success rate')
    plt.plot(range(5, 13), moves_avgs, label='Moves avg')

    plt.xlabel('Number of moves')
    plt.ylabel('Success rate (%)')
    plt.legend()

    plt.show()
