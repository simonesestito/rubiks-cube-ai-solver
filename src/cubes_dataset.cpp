#include "cube.h"
#include "cubes_map.hpp"

#include <iostream>
#include <fstream>
#include <filesystem>

struct CubeSample
{
    uint8_t cube[MAX_MOVES_STAGES - MINUS_MOVES][6][2][2];
    char move;
};

size_t sample_size = (
    (MAX_MOVES_STAGES - MINUS_MOVES)  // how many cubes are in one sample
    * 1  // cube cell
    * 6  // faces
    * 2  // rows
    * 2  // cols
    + 1  // move
);

extern "C" size_t get_cubes_len(const char* filename) {
    // Get the size of the file, divided by sample_size
    std::ifstream stream(filename, std::ios::binary | std::ios::in);
    stream.seekg(0, std::ios::end);
    size_t file_size = stream.tellg();
    stream.close();
    return file_size / sample_size;
}

/**
 * Read cubes LIST from a file on disk.
 * Follow the same binary format as save_cube_to_file.
 */
extern "C" int read_cube(CubeSample *sample, const char *filename, const size_t sample_no)
{
    std::ifstream stream(filename, std::ios::binary | std::ios::in);
    // Since each sample is X bytes long, we can seek to the
    // correct position in the file by multiplying the sample
    // size by the sample number.
    //
    // Check if the file is big enough
    stream.seekg(0, std::ios::end);
    size_t file_size = stream.tellg();
    if (sample_no * sample_size >= file_size) {
        return 0;
    }

    stream.seekg(sample_size * sample_no);

    // Read the cube
    for (int i = 0; i < MAX_MOVES_STAGES - MINUS_MOVES; i++) {
        for (int face = 0; face < 6; face++) {
            for (int row = 0; row < 2; row++) {
                for (int col = 0; col < 2; col++) {
                    char c;
                    stream.read(&c, 1);
                    sample->cube[i][face][row][col] = c;
                }
            }
        }
    }

    // Read the move
    char move;
    stream.read(&move, 1);
    sample->move = move;

    stream.close();

    return 1;
}
