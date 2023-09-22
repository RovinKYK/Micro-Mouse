# Micro Mouse Robot

## Overview

This repository contains the code and resources for a Micro Mouse robot designed for maze navigation using Raspberry Pi. The robot is equipped with Time-of-Flight (ToF) sensors, a QMC5883L compass, rotary encoders, and an L298N motor driver for precise control and navigation.

## Features

- **ToF Sensors**: Utilizes Time-of-Flight sensors for accurate distance measurements.
- **QMC5883L Compass**: Incorporates a digital compass for orientation and heading control.
- **Rotary Encoders**: Employs encoders for precise motor control and odometry.
- **Raspberry Pi**: Powered by a Raspberry Pi for high-level processing and control.
- **Flood Fill Algorithm**: Utilizes a flood fill algorithm for efficient maze exploration.

## Capabilities

The Micro Mouse robot showcases the following capabilities:

1. **Maze Navigation**: The robot efficiently navigates through mazes using a combination of ToF sensors, compass, and encoders for obstacle detection and path planning.

2. **Mapping and Localization**: It employs the QMC5883L compass and encoders for mapping the maze layout and localizing itself within the maze.

3. **Dynamic Path Planning**: The flood fill algorithm dynamically plans the optimal path through the maze, adapting to changing conditions or maze layouts.

4. **Real-time Feedback**: The Raspberry Pi provides real-time feedback on sensor data, allowing for on-the-fly adjustments and decision-making.

## Flood Fill Algorithm

The flood fill algorithm is a pathfinding algorithm used to efficiently explore and map a maze. It works by iteratively assigning values to each cell in the maze, representing the number of steps required to reach the goal from that cell. This allows the robot to make informed decisions on which paths to take.
