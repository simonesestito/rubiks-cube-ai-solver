#ifndef CUBES_MAP_HPP
#define CUBES_MAP_HPP

#include <array>
#include <unordered_map>

typedef std::array<uint32_t, 6> StdCube;

struct CubeHasher {
    std::size_t operator()(const StdCube& c) const {
        // From boost::hash_combine
        size_t seed = 0;
        for (auto i : c) {
            seed ^= i + 0x9e3779b9 + (seed << 6) + (seed >> 2);
        }
        return seed;
    }
};

typedef std::unordered_map<StdCube, char, CubeHasher> CubesMap;

void solve_cubes_map(const CubesMap& cubesMap);

// Constant array of all possible moves
const char CUBE_MOVES[12] = { 'f', 'F', 'u', 'U', 'b', 'B', 'l', 'L', 'r', 'R', 'd', 'D' };

const unsigned char MAX_MOVES_STAGES = 7;
const char* MAP_FILENAME = "cubes_map.bin";

#endif // CUBES_MAP_HPP