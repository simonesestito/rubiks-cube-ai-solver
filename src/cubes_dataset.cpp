#include "cube.h"
#include "cubes_map.hpp"

#include <iostream> 
#include <fstream>
#include <filesystem>

struct CubeSample {
    uint8_t cube[6][3][3];
    char move;
};

/**
 * Read cubes LIST from a file on disk.
 * Follow the same binary format as save_cube_to_file.
 */
extern "C" void read_cubes_list(CubeSample* samples, const char* filename, const int batch_no, int limit_batches) {
    std::ifstream stream(filename, std::ios::binary | std::ios::in);

    // Read 64K block at a time
    char buffer[65536];
    stream.seekg(batch_no * 65536);
    stream.read(buffer, 65536);
    std::size_t read_bytes = static_cast<std::size_t>(stream.gcount());

    std::size_t read_file_total = 0;
    unsigned int samples_i = 0;

    while (read_bytes > 0 && limit_batches-- > 0) {
        // Parse current read buffer
        std::size_t cursor = 0;

        // Read all cube entries in the buffer
        while (read_bytes - cursor >= 25) {
            // Read the cube faces, as 6 uint32_t (see cube.h)
            uint32_t faces[6] = {0};
            for (int i = 0; i < 6; i++) {
                faces[i] = static_cast<uint32_t>(static_cast<unsigned char>(buffer[cursor++]));
                faces[i] |= static_cast<uint32_t>(static_cast<unsigned char>(buffer[cursor++]) << 8);
                faces[i] |= static_cast<uint32_t>(static_cast<unsigned char>(buffer[cursor++]) << 16);
                faces[i] |= static_cast<uint32_t>(static_cast<unsigned char>(buffer[cursor++]) << 24);
            }

            // Read the move (char)
            char move = buffer[cursor++];

            // Insert the cube inside our LIST
            T_CUBE cube = (T_CUBE) faces;
            for (int face = 0; face < 6; face++) {
                for (int row = 0; row < 3; row++) {
                    for (int col = 0; col < 3; col++) {
                        samples[samples_i].cube[face][row][col] = GET_CUBE(cube[face], row, col);
                    }
                }
            }
            samples[samples_i].move = get_reverse_move(move);
            samples_i++;
        }

        // Read next buffer chunk, if any
        stream.read(buffer, 65536);
        read_bytes = static_cast<std::size_t>(stream.gcount());
    }

    stream.close();
}