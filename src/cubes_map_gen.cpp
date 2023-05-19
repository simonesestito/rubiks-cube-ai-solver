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

/**
 * Save to a file on disk
 * using a binary format where each cube is saved as 25 bytes:
 * - 24 bytes for the cube (6 faces * 4 bytes per face = uint32_t)
 * - 1 byte for the move (char)
 * 
 * It's also aligned to 64K bytes, so that it can be loaded
 * efficiently from disk.
 */
void save_cube_to_file(const CubesMap& cubes_map, const char* filename) {
    std::cout << "Saving cubes map to file..." << std::endl;
    std::ofstream file(filename, std::ios::binary | std::ios::out);
    std::size_t written_bytes = 0;
    char buffer[65536] = { 0 };

    for (const auto& it : cubes_map) {
        // Encode 6 uint32_t in our buffer
        for (uint32_t face : it.first) {
            // Encode each uint32_t in 4 bytes,
            // endianness independently
            buffer[written_bytes++] = static_cast<char>(face & 0xFF);
            buffer[written_bytes++] = static_cast<char>((face >> 8) & 0xFF);
            buffer[written_bytes++] = static_cast<char>((face >> 16) & 0xFF);
            buffer[written_bytes++] = static_cast<char>((face >> 24) & 0xFF);
        }

        // Encode the move (char)
        buffer[written_bytes++] = it.second;

        // If the buffer is full, write it to the file
        if (65536 - written_bytes < 25) {
            file.write(buffer, 65536);
            written_bytes = 0;
        }
    }

    // Finally, write the remaining bytes
    if (written_bytes > 0)
        file.write(buffer, written_bytes);

    // Close the file
    file.flush();
    file.close();

    std::cout << "Cubes map saved to file" << std::endl;
}

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
void create_cubes_map(CubesMap& result) {
    // Add the solved cube
    StdCube std_cube;
    {
        T_CUBE cube = create_cube();
        std::copy(cube, cube+6, std_cube.begin());
        free(cube);
    }

    // Create the map of the cubes at the previous stage
    auto previous_stage = new CubesMap();

    // Insert the basic cube
    result.try_emplace(std_cube, '\0');
    previous_stage->try_emplace(std_cube, '\0');
    std::cout << "Stage 0: 1 new cube" << std::endl;

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
                if (result.find(std_cube) == result.end()) {
                    // Add it to the current stage
                    current_stage->try_emplace(std_cube, move);
                    // Add it to the full map
                    result.try_emplace(std_cube, move);
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
    delete previous_stage;
}

int main() {
    CubesMap cubes_map;
    create_cubes_map(cubes_map);

    // Once the map is created, check if it's valid
    solve_cubes_map(cubes_map);

    // If valid, save it to a file.
    save_cube_to_file(cubes_map, MAP_FILENAME);

    return 0;
}