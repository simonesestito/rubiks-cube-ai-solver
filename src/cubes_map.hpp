#ifndef CUBES_MAP_HPP
#define CUBES_MAP_HPP

#include <array>
#include <unordered_map>

typedef std::array<uint32_t, 6> StdCube;

struct CubeHasher {
    std::size_t operator()(const StdCube& c) const;
};

typedef std::unordered_map<StdCube, char, CubeHasher> CubesMap;

// Constant array of all possible moves
static const char CUBE_MOVES[12] = { 'f', 'F', 'u', 'U', 'b', 'B', 'l', 'L', 'r', 'R', 'd', 'D' };

static const unsigned char MAX_MOVES_STAGES = 7;
static const char* MAP_FILENAME = "cubes_map.bin";

/**
 * Get the reverse action of a move.
 */
char get_reverse_move(char move);

/**
 * Given a map of possible cubes, solve them all,
 * using cubes already solved in the map.
 * 
 * This is useful to check if a map is valid.
 */
void solve_cubes_map(const CubesMap& cubesMap);

#endif // CUBES_MAP_HPP