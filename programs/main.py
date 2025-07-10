from kociemba import solve # ruibk's cube solving module
from vision import get_cube_state # module for computer vision
from arduino_comm import perform_rotation # module for communicating with the arduinos

perform_rotation("U2'")
perform_rotation("B2'")
perform_rotation("L")
perform_rotation("R'")
perform_rotation("F2")
