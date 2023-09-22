# Micro Mouse Simulation and Implementation

## TODO
 
 
### Algorithm

- [x] Basic flood fill algorithm
- [x] Basic wall sensing and movements
- [ ] Add rotation movement
- [ ] Add support to arbitrary start location - Currently assumes mouse starts at lower left - corner. The Mouse needs move until enough information is available to determine to location of - the center square
- [ ] Add detection of four center squares
- [ ] Find (or modify) and existing code to visualize movements
- [ ] Find (or modify) and existing code to draw mazes
- [ ] Implement search run back to start square. Ideally mapping most of the maze
- [ ] Implement fast run (using the finalized flood fill values)
- [ ] Optimize flood fill algorithm to reduce search time (dang2010)
- [ ] Implement oblique sprint algorithm (yuan2018)

#### Maze visualizer

Maze files https://github.com/micromouseonline/micromouse_maze_tool
mms simulator https://github.com/mackorone/mms

- [ ] Convert maze files current implementation
- [ ] Convert current implementation to match format given in mms simulator

### Interface

- [ ] PWM
- [ ] PID
- [ ] Get sensor readings (ToF, JVP)
- [ ] Implement wall detection
- [ ] Rotations (90-V, 90-T, 45-T, etc)
- [ ] Implement simulation code
- [ ] ...

### Hardware

- [ ] Finish prototype
- [ ] Testing, testing, and more testing
- [ ] ...
