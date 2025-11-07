# RRT Path Planning Demo (Pygame)

This repository contains a single Python script, `rrt.py`, that visualizes a
basic **Rapidly-exploring Random Tree (RRT)** in 2D using Pygame. The script
spawns random rectangular obstacles, a random start point, and a random goal
point, then grows an RRT until it finds a path close to the goal. When a path
is found, it is highlighted.

- Random start/goal placement
- Random rectangular obstacles
- Incremental RRT growth
- Simple nearest-extension step
- Path reconstruction and drawing once the goal is reached
- Live visualization in a Pygame window
