#include "BitWriter.hpp"

BitWriter::BitWriter(uint8_t* outputBuffer) {
    buffer = outputBuffer;
    bitPosition = 0;
    byteIndex = 0;
}

void BitWriter::writeBits(uint8_t value, int numBits) {
    while (numBits > 0) {
        const int bitsRemaining = 8 - bitPosition;
        const int bitsToWrite = (numBits < bitsRemaining) ? numBits : bitsRemaining;
        const uint8_t mask = (1 << bitsToWrite) - 1;

        buffer[byteIndex] |= (value & mask) << (bitsRemaining - bitsToWrite);

        bitPosition += bitsToWrite;
        numBits -= bitsToWrite;

        if (bitPosition == 8) {
            bitPosition = 0;
            byteIndex++;
        }
    }
}


#include <iostream>

int main() {
    uint8_t buffer[9] = { 0 };
    BitWriter writer(buffer);

    writer.writeBits(0x5, 3);
    writer.writeBits(0xA, 4);
    writer.writeBits(0x7, 3);

    for (int i = 0; i < 9; i++) {
        std::cout << "Buffer[" << i << "]: " << std::hex << static_cast<int>(buffer[i]) << std::endl;
    }

    return 0;
}


