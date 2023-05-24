#include "cube.h"
#include "cubes_map.hpp"
#include <iostream>

/**
 * Hash function for StdCube.
 */
std::size_t CubeHasher::operator()(const StdCube& c) const {
    // From boost::hash_combine
    std::size_t seed = 0;
    for (auto i : c) {
        seed ^= i + 0x9e3779b9 + (seed << 6) + (seed >> 2);
    }
    return seed;
}

/**
 * Get the reverse action of a move.
 */
char get_reverse_move(char move) {
    if (move < 'a') {
        // Make lowercase
        return move - 'A' + 'a';
    } else {
        // Make uppercase
        return move - 'a' + 'A';
    }
}

/**
 * Given a map of possible cubes, solve them all,
 * using cubes already solved in the map.
 * 
 * This is useful to check if a map is valid.
 */
void solve_cubes_map(const CubesMap& cubesMap) {
    // Check if every cube is solvable
    std::cout << "Trying to solve " << cubesMap.size() << " cubes..." << std::endl;

    std::size_t s = 0;
    for (const auto& it : cubesMap) {
        // Show progress
        std::cout << s++ << '\r';

        // Copy the cube from the map
        StdCube std_cube = it.first;
        char move = it.second;

        // Debugging block
        if (is_solved(std_cube.data())) {
            // If the cube is already solved, ERROR
            std::cout << std::endl << "ERROR: Cube already solved" << std::endl;
            // Print each number of the cube
            std::cout << "Cube: ";
            for (int i = 0; i < 6; i++) {
                std::cout << (int) std_cube[i] << ' ';
            }
            std::cout << std::endl;

            // Print each number of the default cube
            T_CUBE cube = create_cube();
            std::cout << "Default cube: ";
            for (int i = 0; i < 6; i++) {
                std::cout << (int) cube[i] << ' ';
            }
            std::cout << std::endl;
            free(cube);
        }

        // Until the cube is solved
        while (is_solved(std_cube.data()) == 0) {
            // Apply the reversed move
            char reverse = get_reverse_move(move);
            perform_action_short(std_cube.data(), reverse);

            if (is_solved(std_cube.data())) {
                break;
            }

            // Go to the next cube
            // If the cube is not in the map, this will crash
            move = cubesMap.find(std_cube)->second;
        }
    }
}