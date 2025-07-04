from kociemba import solve # ruibk's cube solving module
from vision import get_cube_state # module for computer vision

cube = get_cube_state()
actions = solve(cube)

print(actions)