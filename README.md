# pacman
This is an **AI Pacman** game with increasing difficulty on the map through 4 levels. Given a map, players have to use algorithms to define all Pacman movements so that Pacman can eat every fruit and avoid facing monsters. The number of steps in Pacman movements should be as small as possible.
- Level 1: map contains only wall and fruits.
- Level 2: map contains wall, static monsters and fruits.
- Level 3: map contains wall, dynamic monsters (can move at most 2 step to any direction from the beginning position) and fruits. Pacman can only see 9 cells around it.
- Level 4: monsters can chase the Pacman. 

At level 1-2-3, A start algorithm is adopted to generate the shortest path.\
At level 3, Pacman is designed to have a memory to store the observed path in the map.\
At level 4, Minimax and Alpha-Beta pruning algorithms are applied to achieve the best results.
