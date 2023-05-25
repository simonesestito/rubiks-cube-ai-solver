'''
Try to solve cubes using the already known solutions within 8 moves.

Will it be able to solve cubes that are not in the database?
'''

import torch.nn as nn
import cubes_dataset

cells_per_face = 2*2
faces_per_cube = 6
possible_moves = len(cubes_dataset.CUBE_MOVES_ENCODING)

# create the model
class CubeModel(nn.Module):
    def __init__(self):
        super().__init__()
        hidden_layer_size = 128 # cells_per_face * faces_per_cube * 12

        hidden_layers = [
            nn.Linear(hidden_layer_size, hidden_layer_size),
            nn.ReLU(),
        ] * 3

        self.lstm = nn.LSTM(24, hidden_layer_size, num_layers=3, batch_first=True)

        self.mlp = nn.Sequential(
            *hidden_layers,
            nn.Linear(hidden_layer_size, possible_moves),
        )
        self.flatten = nn.Flatten()

    def forward(self, cubes_seq):
        _, (final_state, _) = self.lstm(cubes_seq)
        return self.mlp(final_state[-1])
