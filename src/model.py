'''
Try to solve cubes using the already known solutions within 8 moves.

Will it be able to solve cubes that are not in the database?
'''

import torch
import torch.nn as nn
import torch.nn.functional as F

cells_per_face = 9
faces_per_cube = 6
possible_moves = 12

# create the model
class CubeModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.mlp = nn.Sequential(
            nn.Linear(cells_per_face * faces_per_cube, 64),
            nn.Sigmoid(),
            nn.Linear(64, 64),
            nn.Sigmoid(),
            nn.Linear(64, possible_moves),
        )
        self.flatten = nn.Flatten()

    def forward(self, x):
        x = self.flatten(x)
        return self.mlp(x)