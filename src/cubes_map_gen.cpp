/**
 * List of all cubes solvable in at most MAX_MOVES_STAGES moves.
 *
 * To achieve this, we start from the solved cube and perform all possible
 * moves, MAX_MOVES_STAGES times. This gives us a list of all cubes solvable in at most 7 moves.
 *
 * Also, we need to efficiently save those cubes,
 * so we use an unordered_map, and the value will be the number of moves required.
 */

#include "cube.h"
#include "cubes_map.hpp"

#include <iostream>
#include <fstream>
#include <unordered_set>


/**
 * Create a map of all cubes solvable in at most MAX_MOVES_STAGES moves.
 * 
 * This uses a breadth-first approach.
 * We calculate all the possible moves from the previous stage,
 * keeping information about only the new cubes (collisions are possible).
 * So, at the next stage, we can work only on those new cubes.
 * 
 * A recursive approach would be fundamentally wrong,
 * because a depth-first approach wouldn't necessary
 * keep only the shortest move for the cube.
 */
void create_cubes_map() {
    // Add the solved cube
    StdCube std_cube;
    {
        T_CUBE cube = create_cube();
        std::copy(cube, cube+6, std_cube.begin());
        free(cube);
    }

    auto all_cubes_map = new CubesMap();

    // Create the map of the cubes at the previous stage
    auto previous_stage = new CubesMap();
    auto all_cubes = std::unordered_set<StdCube, CubeHasher>();

    // Insert the basic cube
    previous_stage->try_emplace(std_cube, '\0');
    all_cubes.insert(std_cube);

    // For each stage, add all the possible moves
    // to the previous stage new cubes.
    for (int i = 1; i <= MAX_MOVES_STAGES; i++) {
        // Create the map of the cubes at the current stage
        auto current_stage = new CubesMap();

        // For each cube at the previous stage
        for (const auto& it : *previous_stage) {
            // For each possible move
            for (const char move : CUBE_MOVES) {
                // Apply the move, copying the old cube and then moving it
                std_cube = it.first;
                perform_action_short(std_cube.data(), move);

                // If the cube is not already in the map
                if (all_cubes.find(std_cube) == all_cubes.end()) {
                    // Add it to the current stage
                    current_stage->try_emplace(std_cube, get_reverse_move(move));
                    // Add it to the full map
                    all_cubes.insert(std_cube);
                    all_cubes_map->try_emplace(std_cube, get_reverse_move(move));
                }
            }
        }

        // Show progress
        std::cout << "Stage " << i << ": " << current_stage->size() << " new cubes" << std::endl;

        // Delete the previous stage
        delete previous_stage;
        // Set the current stage as the previous stage
        previous_stage = current_stage;
    }

    // Finally, count the number of moves for a cube from last step
    int moves_count = 0;
    for (const auto& initial : *previous_stage) {
        // Create a copy of the cube
        std_cube = initial.first;
        char move = initial.second;

        // While the cube is not solved
        while (!is_solved(std_cube.data())) {
            // Apply the move
            perform_action_short(std_cube.data(), move);
            moves_count++;

            if (is_solved(std_cube.data()))
                break;

            // Get the next move
            move = all_cubes_map->find(std_cube)->second;
        }


        break;
    }


    // For each cube in previous_stage, save all the previous cubes
    // in a final file
    std::ofstream file("cubes_map.bin", std::ios::binary | std::ios::out);
    int it_written = 0;
    for (const auto& it : *previous_stage) {
        it_written++;
        // Create a copy of the cube
        std_cube = it.first;
        char move = it.second;

        int bytes_written = 0;

        // For only the amount of moves requested...
        for (int _ = 0; _ < MAX_MOVES_STAGES-MINUS_MOVES; _++) {
            // Save the cube to the file
            for (int face = 0; face < 6; face++) {
                for (int row = 0; row < 2; row++) {
                    for (int col = 0; col < 2; col++) {
                        char c = GET_CUBE(std_cube.data()[face], row, col);
                        file.write(&c, 1);
                        bytes_written++;
                    }
                }
            }

            // Apply the move
            perform_action_short(std_cube.data(), move);

            // Get the next move
            move = all_cubes_map->find(std_cube)->second;
        }

        // After having written all the cubes, write the last move
        file.write(&move, 1);
        bytes_written++;
    }

    file.flush();
    file.close();
    std::cout << "Written " << it_written << " cubes" << std::endl;

    std::cout << "Cubes map created, " << previous_stage->size() << " cubes, " << moves_count << " moves" << std::endl;

    delete previous_stage;
}

int main() {
    // Create the maxi list


    create_cubes_map();

    // Once the map is created, check if it's valid
    // TODO: solve_cubes_map(cubes_map);

    // If valid, save it to a file.
    // TODO: save_cube_to_file(cubes_map, MAP_FILENAME);

    return 0;
}
