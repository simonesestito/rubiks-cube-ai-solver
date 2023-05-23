'''
Try to solve cubes using the already known solutions within 8 moves.

Will it be able to solve cubes that are not in the database?
'''

import torch
import torch.nn as nn
import torch.nn.functional as F
import cubes_dataset

cells_per_face = 9
faces_per_cube = 6
possible_moves = len(cubes_dataset.CUBE_MOVES_ENCODING)

# create the model
class CubeModel(nn.Module):
    def __init__(self):
        super().__init__()
        hidden_layer_size = faces_per_cube * 13 * 2

        hidden_layers = [
            nn.Linear(hidden_layer_size, hidden_layer_size),
            nn.Sigmoid(),
        ] * 13

        self.mlp = nn.Sequential(
            nn.Linear(cells_per_face * faces_per_cube, hidden_layer_size),
            nn.Sigmoid(),
            *hidden_layers,
            nn.Linear(hidden_layer_size, possible_moves),
        )
        self.flatten = nn.Flatten()

    def forward(self, x):
        x = self.flatten(x)
        return self.mlp(x)