#ifndef BIT_READER_HPP
#define BIT_READER_HPP

#include <cstdint>

class BitReader {
private:
    const uint8_t* buffer;
    int bitPosition;
    int byteIndex;

public:
    BitReader(const uint8_t* inputBuffer);
    uint8_t readBits(int numBits);
};

#endif  // BIT_READER_HPP

