#include "cube.h"
#include "cubes_map.hpp"

#include <iostream> 
#include <fstream>
#include <filesystem>

/**
 * Read cubes map from a file on disk.
 * Follow the same binary format as save_cube_to_file.
 */
void read_cubes_map(CubesMap& result, const char* filename) {
    std::cout << "Reading cubes map from file " << filename << "..." << std::endl;
    std::ifstream stream(filename, std::ios::binary | std::ios::in);

    // Read 64K block at a time
    char buffer[65536];
    stream.read(buffer, 65536);
    std::size_t read_bytes = static_cast<std::size_t>(stream.gcount());

    std::filesystem::path file_path{filename};
    std::uintmax_t file_size = std::filesystem::file_size(file_path);
    std::uintmax_t read_file_total = 0;

    while (read_bytes > 0) {
        // Parse current read buffer
        std::size_t cursor = 0;

	// Update read progress
	read_file_total += read_bytes;
	printf("Reading cubes map... (%.1f%%)\r", read_file_total*1.0 / file_size * 100.0);

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

            // Insert the cube inside our map
            StdCube std_cube;
            std::copy(std::begin(faces), std::end(faces), std_cube.begin());
            result[std_cube] = move;
        }

        // Read next buffer chunk, if any
        stream.read(buffer, 65536);
        read_bytes = static_cast<std::size_t>(stream.gcount());
    }
    std::cout << std::endl;

    stream.close();
}

extern "C" CubesMap* load_cubes_map(const char* filename) {
    CubesMap* result = new CubesMap();
    read_cubes_map(*result, filename);
    return result;
}

extern "C" char get_cube_from_map(const CubesMap* result, const T_CUBE cube) {
    StdCube std_cube;
    // The upper 5 bits of each face are not used,
    // but we need to set them to 0, otherwise the
    // hash will be different.
    for (int i = 0; i < 6; i++) {
        std_cube[i] = cube[i] & 0x7ffffff; // Lower 27 bits
    }

    auto it = result->find(std_cube);
    if (it == result->end()) {
        // Cube not found in the map
        return '-'; // Don't use \0, it will be interpreted as a solved cube
    } else {
        return get_reverse_move(it->second);
    }
}

extern "C" void free_cubes_map(CubesMap* result) {
    delete result;
}
