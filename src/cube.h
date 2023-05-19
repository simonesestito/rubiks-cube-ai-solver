#ifndef CUBE_H
#define CUBE_H

#include <stdint.h>

#define T_CUBE_FACE uint32_t
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