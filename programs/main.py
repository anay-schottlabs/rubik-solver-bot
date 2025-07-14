from kociemba import solve # ruibk's cube solving module
from vision import get_cube_state # module for computer vision
from arduino_comm import perform_algorithm, close_connections # module for communicating with the arduinos

cube_state = get_cube_state()  # Get the current state of the cube
alg_str = solve(cube_state)  # Determine algorithm to solve the cube

print(f"Solution algorithm: {alg_str}") # Print the algorithm out

perform_algorithm(alg_str)  # Run the algorithm to solve the cube

close_connections() # Close the connections to the arduinos
