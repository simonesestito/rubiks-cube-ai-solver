# Rubik's Cube AI Solver
Rubik's Cube solver that reads photos using OpenCV and solves it using LTSM (Long Short Term Memory) model. Built using PyTorch.

<a href="https://raw.githubusercontent.com/simonesestito/rubiks-cube-ai-solver/main/Final_Report.pdf">
    <img src=".github/assets/report-button.svg" alt="Download Report">
</a>
<a href="https://raw.githubusercontent.com/simonesestito/rubiks-cube-ai-solver/main/Presentation.pdf">
    <img src=".github/assets/presentation-button.svg" alt="Download Presentation">
</a>

# OpenCV

This is the part of the project that works with OpenCV.

Given a set of photos, it will recognize the cube and (hopefully) solve it optimally.

---

There is also an Artifical Intelligence part (Pytorch and the LSTM model) which works on 2x2 cubes.
Checkout the **main** branch for that!

# Project Usage (OpenCV part)
1. Clone this repository and `cd` into it
2. Run `make clean && make` to compile all native code (Linux is required!)
3. Download the pre-built dataset from our [Google Drive folder](https://drive.google.com/file/d/1T30Le0Q1SPz30vyvtRFDaCmAP9aPVdbj/view?usp=drivesdk)
- The file must be put in the root project directory, which is also the current working directory
- You can also build it by yourself running `./src/cubes_map_gen`, however it will require some hours and lots of GBs of RAM
4. Choose a cube from those in the `assets/images/` folder (from _cube-0_ to _cube-9_), then run `python3 src/main.py CUBE_YOU_CHOSE`: you will see all the moves required to solve it.

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
