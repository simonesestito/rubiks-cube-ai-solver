# Rubik's Cube AI Solver
Rubik's Cube solver that reads photos using OpenCV and solves it using LTSM (Long Short Term Memory) model. Built using PyTorch.

<a href="https://raw.githubusercontent.com/simonesestito/rubiks-cube-ai-solver/main/Final_Report.pdf">
    <img src=".github/assets/report-button.svg" alt="Download Report">
</a>
<a href="https://raw.githubusercontent.com/simonesestito/rubiks-cube-ai-solver/main/Presentation.pdf">
    <img src=".github/assets/presentation-button.svg" alt="Download Presentation">
</a>

## OpenCV

It also contains a visual part using OpenCV: please checkout **opencv** branch for that.

# Project Usage (AI part)
1. Clone this repository and `cd` into it
2. Run `make clean && make` to compile all native code (Linux is required!)
3. Run `./src/cubes_map_gen`
4. [Not recommended] You can run the training with `python3 src/training.py` or use the pre-trained _model.ckpt_ file
5. Run `python3 src/real_world_test.py` to execute tests on random real world cubes
6. Run `python3 src/evaluation.py` for a more advanced cross-validation (~2-3 hours required on GPU)

## License
Copyright (C) 2023
[Simone Sestito](https://github.com/simonesestito),
[Sabrina Troili](https://github.com/SabrinaTroili),
[Alessandro Scifoni](https://github.com/ernutella001).

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
