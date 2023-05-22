import cube_tests
from cubes_map import CubesMap
from progressbar import progressbar

if __name__ == '__main__':
    TOT_CUBES = 100*1000

    cubes_map = CubesMap()
    unsolved_cubes = 0

    for _ in progressbar(range(TOT_CUBES)):
        random_cube, _ = cube_tests.randomize_cube(n_moves=20)
        if cubes_map[random_cube] is None:
            unsolved_cubes += 1

    print(f'Unsolved {unsolved_cubes} / {TOT_CUBES} (= {(unsolved_cubes/TOT_CUBES*100):.2f}%)')