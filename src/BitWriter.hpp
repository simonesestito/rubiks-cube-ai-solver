#include <cstdint>

class BitWriter {
private:
    uint8_t* buffer;
    int bitPosition;
    int byteIndex;

public:
    BitWriter(uint8_t* outputBuffer);
    void writeBits(uint8_t value, int numBits);
};


