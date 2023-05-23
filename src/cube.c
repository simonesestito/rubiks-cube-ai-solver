/**
    C implementation of the cube simulator.

    You need to compile it using the following command (on Linux):
    make # from the root directory
*/

#include <string.h>
#include <stdlib.h>
#include "cube.h"

void reset_cube(T_CUBE cube);

T_CUBE create_cube() {
    // Remember to free the cube!
    T_CUBE cube = (T_CUBE) malloc(6 * sizeof(T_CUBE_FACE));
    reset_cube(cube);
    return cube;
}

T_CUBE create_cube_from(uint8_t* flatten_faces) {
    T_CUBE cube = (T_CUBE) malloc(6 * sizeof(T_CUBE_FACE));

    // Zero out the cube
    memset(cube, 0, 6 * sizeof(T_CUBE_FACE));

    // Copy the faces into the cube
    for (uint8_t face = 0; face < 6; face++) {
        for (uint8_t row = 0; row < 2; row++) {
            for (uint8_t col = 0; col < 2; col++) {
                uint8_t i = face * 4 + row * 2 + col;
                SET_CUBE(cube[face], row, col, flatten_faces[i]);
            }
        }
    }

    return cube;
}

void reset_cube(T_CUBE cube) {
    for (T_CUBE_CELL face = 0; face < 6; face++) {
        for (T_CUBE_CELL row = 0; row < 2; row++) {
            for (T_CUBE_CELL col = 0; col < 2; col++) {
                SET_CUBE(cube[face], row, col, face);
            }
        }
    }
}

void perform_action_short(T_CUBE cube, char action) {
    switch (action) {
        case 'F': face0_clock(cube); break;
        case 'R': face3_clock(cube); break;
        case 'U': face1_clock(cube); break;
        case 'B': face5_clock(cube); break;
        case 'L': face2_clock(cube); break;
        case 'D': face4_clock(cube); break;
        case 'f': face0_counterclock(cube); break;
        case 'r': face3_counterclock(cube); break;
        case 'u': face1_counterclock(cube); break;
        case 'b': face5_counterclock(cube); break;
        case 'l': face2_counterclock(cube); break;
        case 'd': face4_counterclock(cube); break;
    }
}

void rotate_clock(T_CUBE cube, uint8_t face) {
    // Step 1: Transpose the matrix
    for (uint8_t i = 0; i < 2; i++) {
        for (uint8_t j = i + 1; j < 2; j++) {
            T_CUBE_CELL temp = GET_CUBE(cube[face], i, j);
            SET_CUBE(cube[face], i, j, GET_CUBE(cube[face], j, i));
            SET_CUBE(cube[face], j, i, temp);
        }
    }

    // Step 2: Reverse the rows of the transposed matrix
    for (uint8_t i = 0; i < 2; i++) {
        for (uint8_t j = 0; j < 1; j++) {
            T_CUBE_CELL temp = GET_CUBE(cube[face], i, j);
            SET_CUBE(cube[face], i, j, GET_CUBE(cube[face], i, 1-j));
            SET_CUBE(cube[face], i, 1-j, temp);
        }
    }
}

void rotate_counterclock(T_CUBE cube, uint8_t face) {
    // Step 1: Transpose the matrix
    for (uint8_t i = 0; i < 2; i++) {
        for (uint8_t j = i + 1; j < 2; j++) {
            T_CUBE_CELL temp = GET_CUBE(cube[face], i, j);
            SET_CUBE(cube[face], i, j, GET_CUBE(cube[face], j, i));
            SET_CUBE(cube[face], j, i, temp);
        }
    }

    // Step 2: Reverse the columns of the transposed matrix
    for (uint8_t i = 0; i < 2; i++) {
        for (uint8_t j = 0; j < 1; j++) {
            T_CUBE_CELL temp = GET_CUBE(cube[face], j, i);
            SET_CUBE(cube[face], j, i, GET_CUBE(cube[face], 1-j, i));
            SET_CUBE(cube[face], 1-j, i, temp);
        }
    }
}

void face0_clock(T_CUBE cube) {
    // Rotate current face
    rotate_clock(cube, 0);

    // Adjust adjacent faces, swapping the rows.
    // Numbers represent the moved face, letters the side;
    //      B = bottom row, T = top row, L = left column, R = right column.
    // Note: index order is (row, column)
    
    T_CUBE_FACE old[6];
    memcpy(old, cube, sizeof(old));

    for (T_CUBE_CELL i = 0; i < 2; i++) {
        // Perform swaps!
        SET_CUBE(cube[1], 1, i, GET_CUBE(old[2], 1-i, 1));
        SET_CUBE(cube[3], i, 0, GET_CUBE(old[1], 1, i));
        SET_CUBE(cube[4], 0, i, GET_CUBE(old[3], 1-i, 0));
        SET_CUBE(cube[2], i, 1, GET_CUBE(old[4], 0, i));
    }
}

void face0_counterclock(T_CUBE cube) {
    // Rotate current face
    rotate_counterclock(cube, 0);

    // Adjust adjacent faces, swapping the rows.
    // Numbers represent the moved face, letters the side;
    //      B = bottom row, T = top row, L = left column, R = right column.
    // Note: index order is (row, column)
    
    // 0 -> 1b,3l,4t,2r
    T_CUBE_FACE old[6];
    memcpy(old, cube, sizeof(old));

    for (T_CUBE_CELL i = 0; i < 2; i++) {
        // Perform swaps!
        SET_CUBE(cube[1], 1, i, GET_CUBE(old[3], i, 0));
        SET_CUBE(cube[3], i, 0, GET_CUBE(old[4], 0, 1-i));
        SET_CUBE(cube[4], 0, i, GET_CUBE(old[2], i, 1));
        SET_CUBE(cube[2], i, 1, GET_CUBE(old[1], 1, 1-i));
    }
}

void face1_clock(T_CUBE cube) {
    // Same logic as face0_clock, but with different swaps.
    rotate_clock(cube, 1);

    // 1 -> 0t,2t,5t,3t
    T_CUBE_FACE old[6];
    memcpy(old, cube, sizeof(old));

    for (T_CUBE_CELL i = 0; i < 2; i++) {
        // Perform swaps!
        SET_CUBE(cube[0], 0, i, GET_CUBE(old[3], 0, i));
        SET_CUBE(cube[2], 0, i, GET_CUBE(old[0], 0, i));
        SET_CUBE(cube[5], 0, i, GET_CUBE(old[2], 0, i));
        SET_CUBE(cube[3], 0, i, GET_CUBE(old[5], 0, i));
    }
}

void face1_counterclock(T_CUBE cube) {
    // Same logic as face0_counterclock, but with different swaps.
    rotate_counterclock(cube, 1);

    // 1 -> 0t,2t,5t,3t
    T_CUBE_FACE old[6];
    memcpy(old, cube, sizeof(old));

    for (T_CUBE_CELL i = 0; i < 2; i++) {
        // Perform swaps!
        SET_CUBE(cube[0], 0, i, GET_CUBE(old[2], 0, i));
        SET_CUBE(cube[2], 0, i, GET_CUBE(old[5], 0, i));
        SET_CUBE(cube[5], 0, i, GET_CUBE(old[3], 0, i));
        SET_CUBE(cube[3], 0, i, GET_CUBE(old[0], 0, i));
    }
}

void face2_clock(T_CUBE cube) {
    // Same logic as face0_clock, but with different swaps.
    rotate_clock(cube, 2);

    // 2 -> 0l,4l,5r,1l
    T_CUBE_FACE old[6];
    memcpy(old, cube, sizeof(old));

    for (T_CUBE_CELL i = 0; i < 2; i++) {
        // Perform swaps!
        SET_CUBE(cube[0], i, 0, GET_CUBE(old[1], i, 0));
        SET_CUBE(cube[4], i, 0, GET_CUBE(old[0], i, 0));
        SET_CUBE(cube[5], i, 1, GET_CUBE(old[4], 1-i, 0));
        SET_CUBE(cube[1], i, 0, GET_CUBE(old[5], 1-i, 1));
    }
}

void face2_counterclock(T_CUBE cube) {
    // Same logic as face0_counterclock, but with different swaps.
    rotate_counterclock(cube, 2);

    // 2 -> 0l,4l,5r,1l
    T_CUBE_FACE old[6];
    memcpy(old, cube, sizeof(old));

    for (T_CUBE_CELL i = 0; i < 2; i++) {
        // Perform swaps!
        SET_CUBE(cube[0], i, 0, GET_CUBE(old[4], i, 0));
        SET_CUBE(cube[4], i, 0, GET_CUBE(old[5], 1-i, 1));
        SET_CUBE(cube[5], i, 1, GET_CUBE(old[1], 1-i, 0));
        SET_CUBE(cube[1], i, 0, GET_CUBE(old[0], i, 0));
    }
}

void face3_clock(T_CUBE cube) {
    // Same logic as face0_clock, but with different swaps.
    rotate_clock(cube, 3);

    // 3 -> 0r,1r,5l,4r
    T_CUBE_FACE old[6];
    memcpy(old, cube, sizeof(old));

    for (T_CUBE_CELL i = 0; i < 2; i++) {
        // Perform swaps!
        SET_CUBE(cube[0], i, 1, GET_CUBE(old[4], i, 1));
        SET_CUBE(cube[1], i, 1, GET_CUBE(old[0], i, 1));
        SET_CUBE(cube[5], i, 0, GET_CUBE(old[1], 1-i, 1));
        SET_CUBE(cube[4], i, 1, GET_CUBE(old[5], 1-i, 0));
    }
}

void face3_counterclock(T_CUBE cube) {
    // Same logic as face0_counterclock, but with different swaps.
    rotate_counterclock(cube, 3);

    // 3 -> 0r,1r,5l,4r
    T_CUBE_FACE old[6];
    memcpy(old, cube, sizeof(old));

    for (T_CUBE_CELL i = 0; i < 2; i++) {
        // Perform swaps!
        SET_CUBE(cube[0], i, 1, GET_CUBE(old[1], i, 1));
        SET_CUBE(cube[1], i, 1, GET_CUBE(old[5], 1-i, 0));
        SET_CUBE(cube[5], i, 0, GET_CUBE(old[4], 1-i, 1));
        SET_CUBE(cube[4], i, 1, GET_CUBE(old[0], i, 1));
    }
}

void face4_clock(T_CUBE cube) {
    // Same logic as face0_clock, but with different swaps.
    rotate_clock(cube, 4);

    // 4 -> 0b,3b,5b,2b
    T_CUBE_FACE old[6];
    memcpy(old, cube, sizeof(old));

    for (T_CUBE_CELL i = 0; i < 2; i++) {
        // Perform swaps!
        SET_CUBE(cube[0], 1, i, GET_CUBE(old[2], 1, i));
        SET_CUBE(cube[3], 1, i, GET_CUBE(old[0], 1, i));
        SET_CUBE(cube[5], 1, i, GET_CUBE(old[3], 1, i));
        SET_CUBE(cube[2], 1, i, GET_CUBE(old[5], 1, i));
    }
}

void face4_counterclock(T_CUBE cube) {
    // Same logic as face0_counterclock, but with different swaps.
    rotate_counterclock(cube, 4);

    // 4 -> 0b,3b,5b,2b
    T_CUBE_FACE old[6];
    memcpy(old, cube, sizeof(old));

    for (T_CUBE_CELL i = 0; i < 2; i++) {
        // Perform swaps!
        SET_CUBE(cube[0], 1, i, GET_CUBE(old[3], 1, i));
        SET_CUBE(cube[3], 1, i, GET_CUBE(old[5], 1, i));
        SET_CUBE(cube[5], 1, i, GET_CUBE(old[2], 1, i));
        SET_CUBE(cube[2], 1, i, GET_CUBE(old[0], 1, i));
    }
}

void face5_clock(T_CUBE cube) {
    // Same logic as face0_clock, but with different swaps.
    rotate_clock(cube, 5);

    // 5 -> 1t,2l,4b,3r
    T_CUBE_FACE old[6];
    memcpy(old, cube, sizeof(old));

    for (T_CUBE_CELL i = 0; i < 2; i++) {
        // Perform swaps!
        SET_CUBE(cube[1], 0, i, GET_CUBE(old[3], i, 1));
        SET_CUBE(cube[2], i, 0, GET_CUBE(old[1], 0, 1-i));
        SET_CUBE(cube[4], 1, i, GET_CUBE(old[2], i, 0));
        SET_CUBE(cube[3], i, 1, GET_CUBE(old[4], 1, 1-i));
    }
}

void face5_counterclock(T_CUBE cube) {
    // Same logic as face0_counterclock, but with different swaps.
    rotate_counterclock(cube, 5);

    // 5 -> 1t,2l,4b,3r
    T_CUBE_FACE old[6];
    memcpy(old, cube, sizeof(old));

    for (T_CUBE_CELL i = 0; i < 2; i++) {
        // Perform swaps!
        SET_CUBE(cube[4], 1, i, GET_CUBE(old[3], 1-i, 1));
        SET_CUBE(cube[2], i, 0, GET_CUBE(old[4], 1, i));
        SET_CUBE(cube[1], 0, i, GET_CUBE(old[2], 1-i, 0));
        SET_CUBE(cube[3], i, 1, GET_CUBE(old[1], 0, i));
    }
}

void perform_action(T_CUBE cube, char* actions) {
    char* action = strtok(actions, " ");

    while (action != NULL) {
        if (action[1] == '\0') {
            switch (action[0]) {
                case 'F': face0_clock(cube); break;
                case 'R': face3_clock(cube); break;
                case 'U': face1_clock(cube); break;
                case 'B': face5_clock(cube); break;
                case 'L': face2_clock(cube); break;
                case 'D': face4_clock(cube); break;
                case 'f': face0_counterclock(cube); break;
                case 'r': face3_counterclock(cube); break;
                case 'u': face1_counterclock(cube); break;
                case 'b': face5_counterclock(cube); break;
                case 'l': face2_counterclock(cube); break;
                case 'd': face4_counterclock(cube); break;
            }
        } else if (action[1] == '\'') {
            switch (action[0]) {
                case 'F': face0_counterclock(cube); break;
                case 'R': face3_counterclock(cube); break;
                case 'U': face1_counterclock(cube); break;
                case 'B': face5_counterclock(cube); break;
                case 'L': face2_counterclock(cube); break;
                case 'D': face4_counterclock(cube); break;
            }
        }

        action = strtok(NULL, " ");
    }
}

//! Need to free the returned array!
uint8_t* _solved_faces(T_CUBE cube) {
    uint8_t* solved = (uint8_t*) malloc(6 * sizeof(uint8_t));

    for (uint8_t face = 0; face < 6; face++) {
        T_CUBE_CELL center = face;

        solved[face] = 0;

        for (uint8_t row = 0; row < 2; row++) {
            for (uint8_t col = 0; col < 2; col++) {

                //* Count solved faces, excluding the center.
                if (GET_CUBE(cube[face], row, col) == center) {
                    solved[face]++;
                }

            }
        }
    }

    return solved;
}

uint8_t solved_faces(T_CUBE cube) {
    // Count solved faces (= 8, without the center).
    uint8_t* solved = _solved_faces(cube);
    uint8_t total = 0;

    for (uint8_t face = 0; face < 6; face++) {
        if (solved[face] == 4) {
            total++;
        }
    }

    free(solved);

    return total;
}

int is_solved(T_CUBE cube) {
    return solved_faces(cube) == 6;
}

double solution_percentage(T_CUBE cube) {
    uint8_t* solved = _solved_faces(cube);
    double total = 0;

    for (uint8_t face = 0; face < 6; face++) {
        total += solved[face];
    }

    free(solved);

    return total / (6 /*faces*/ * 4 /*cells*/);
}

T_CUBE_CELL get_cell(T_CUBE cube, uint8_t face, uint8_t row, uint8_t col) {
    return GET_CUBE(cube[face], row, col);
}