#ifndef CUBE_H
#define CUBE_H

#include <stdint.h>

/*
 * A cube is represented as 6 uint32_t,
 * each for every face of the cube.
 *
 * We need to encode 6 colors, so 3 bits each are enough
 * but we have 4 cells for each face.
 * That adds up to 3*4 = 12 bits, so we use uint16_t
 * for each face.
 * That being said, a cube is an array of 6 uint16_t.
 */

#define GET_CUBE(face, row, col) \
    (((face) >> 3*((row)*3+(col))) & 0b111)

#define SET_CUBE(face, row, col, v) \
    (face) = ((v)&0b111) << 3*((row)*3+(col)) | ((face) & (0xFFFFFFFF ^ (0b111 << 3*((row)*3+(col)))))

#define T_CUBE_FACE uint16_t
#define T_CUBE T_CUBE_FACE*
#define T_CUBE_CELL uint8_t

T_CUBE create_cube();
void perform_action_short(T_CUBE cube, char action);

void face0_clock(T_CUBE cube);
void face0_counterclock(T_CUBE cube);
void face1_clock(T_CUBE cube);
void face1_counterclock(T_CUBE cube);
void face2_clock(T_CUBE cube);
void face2_counterclock(T_CUBE cube);
void face3_clock(T_CUBE cube);
void face3_counterclock(T_CUBE cube);
void face4_clock(T_CUBE cube);
void face4_counterclock(T_CUBE cube);
void face5_clock(T_CUBE cube);
void face5_counterclock(T_CUBE cube);


#endif // CUBE_H