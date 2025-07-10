from kociemba import solve # ruibk's cube solving module
from vision import get_cube_state # module for computer vision
from arduino_comm import perform_rotation, perform_algorithm, close_connections # module for communicating with the arduinos

print("INDEPENDENT MOVES:\n")

perform_rotation("U2'")
perform_rotation("B2'")
perform_rotation("L")
perform_rotation("R'")
perform_rotation("F2")

print("ALGORITHM MOVES:\n")

perform_algorithm("U2 B2 L R' F2")

close_connections()
