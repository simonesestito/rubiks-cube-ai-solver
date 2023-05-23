#include "cube.h"
#include "cubes_map.hpp"

#include <iostream>
#include <fstream>
#include <filesystem>

struct CubeSample
{
    uint8_t cube[6][2][2];
    char move;
};

/**
 * Read cubes LIST from a file on disk.
 * Follow the same binary format as save_cube_to_file.
 */
extern "C" size_t read_cubes_list(CubeSample *samples, const char *filename, const int batch_no, int limit_batches)
{
    std::ifstream stream(filename, std::ios::binary | std::ios::in);

    // Read 64K block at a time
    char buffer[65536];
    stream.seekg(batch_no * 65536);
    stream.read(buffer, 65536);
    std::size_t read_bytes = static_cast<std::size_t>(stream.gcount());

    std::size_t read_file_total = 0;
    size_t samples_i = 0;

    while (read_bytes > 0 && limit_batches-- > 0)
    {
        // Parse current read buffer
        std::size_t cursor = 0;

        // Read all cube entries in the buffer
        while (read_bytes - cursor >= 13)
        {
            // Read the cube faces, as 6 uint16_t (see cube.h)
            uint16_t faces[6] = {0};
            for (int i = 0; i < 6; i++)
            {
                faces[i] = static_cast<uint16_t>(static_cast<unsigned char>(buffer[cursor++]));
                faces[i] |= static_cast<uint16_t>(static_cast<unsigned char>(buffer[cursor++]) << 8);
            }

            // Read the move (char)
            char move = buffer[cursor++];

            // Insert the cube inside our LIST
            T_CUBE cube = (T_CUBE)faces;
            for (int face = 0; face < 6; face++)
            {
                for (int row = 0; row < 2; row++)
                {
                    for (int col = 0; col < 2; col++)
                    {
                        std::cout << "Faces: " << face << " " << row << " " << col << std::endl;
                        std::cout << "Cube: " << cube[face] << std::endl;
                        std::cout << "Samples: " << samples_i << std::endl;
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

    return samples_i;
}

int main() {
    std::cout << "Cubes dataset" << std::endl;

    // Read cubes from file
    CubeSample samples[5041];
    size_t samples_count = read_cubes_list(samples, "cubes_map.bin", 0, 1);

    return 0;
}