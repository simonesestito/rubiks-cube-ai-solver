#include "BitReader.hpp"

BitReader::BitReader(const uint8_t* inputBuffer) {
    buffer = inputBuffer;
    bitPosition = 0;
    byteIndex = 0;
}

uint8_t BitReader::readBits(int numBits) {
    uint8_t result = 0;

    while (numBits > 0) {
        const int bitsRemaining = 8 - bitPosition;
        const int bitsToRead = (numBits < bitsRemaining) ? numBits : bitsRemaining;
        const uint8_t mask = (1 << bitsToRead) - 1;

        result <<= bitsToRead;
        result |= (buffer[byteIndex] >> (bitsRemaining - bitsToRead)) & mask;

        bitPosition += bitsToRead;
        numBits -= bitsToRead;

        if (bitPosition == 8) {
            bitPosition = 0;
            byteIndex++;
        }
    }

    return result;
}

#include <iostream>

int main() {
    uint8_t buffer[9] = { 0xb5, 0xc0, 0x34, 0x78, 0x9A, 0xBC, 0xDE, 0xF0, 0xFF };
    BitReader reader(buffer);

    uint8_t bits = reader.readBits(3);
    std::cout << "Read bits: " << (int) bits << std::endl;

    bits = reader.readBits(4);
    std::cout << "Read bits: " << std::hex << static_cast<int>(bits) << std::endl;

    bits = reader.readBits(3);
    std::cout << "Read bits: " << std::hex << static_cast<int>(bits) << std::endl;

    return 0;
}


