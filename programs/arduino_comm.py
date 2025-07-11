from dotenv import load_dotenv
from os import getenv
import serial

### IMPORTANT NOTE
# This program is quite ambiguous between the two arduinos
# This is done because both arduinos are sent the same message
# The arduino programs then decide which faces of the cube each one is responsible for turning
# When reading responses, the program only cares if either arduino responds with a valid message
# This is because only the arduino that turns the face will respond

# Load environment variables from .env file
load_dotenv(override=True)

# Determine the serial ports for the arduinos
ARDUINO1_PORT = getenv("ARDUINO1_PORT")
ARDUINO2_PORT = getenv("ARDUINO2_PORT")

# Both arduinos are on 9600 baud with a timeout of 1 second
ARDUINO1 = serial.Serial(ARDUINO1_PORT, 9600, timeout=1)
ARDUINO2 = serial.Serial(ARDUINO2_PORT, 9600, timeout=1)

def perform_rotation(move_notation: str) -> None:
    """
    Send a single move notation to both Arduinos and wait for confirmation.

    The function writes the move notation (e.g., "R", "U'", "F2") to both Arduinos.
    Only the Arduino responsible for the move will respond with the same notation.
    The function waits until a valid response is received, indicating the move is complete.

    Args:
        move_notation (str): The move to perform, in standard cube notation.
    """
    print(f"Sending {move_notation}")

    while True:
        # Write the move notation to both arduinos
        ARDUINO1.write(move_notation.encode())
        ARDUINO2.write(move_notation.encode())

        # Read the response from the arduinos
        line1 = ARDUINO1.readline().decode().strip()
        line2 = ARDUINO2.readline().decode().strip()

        # Check if the arduinos responded with a valid message
        if line1 == move_notation or line2 == move_notation:
            print(f"Received {line1 if line1 == move_notation else line2}")
            print("Move completed\n")
            break

def perform_algorithm(algorithm: str) -> None:
    """
    Execute a sequence of cube moves by sending each move to the Arduinos.

    The algorithm string should be a sequence of moves separated by spaces,
    using standard cube notation (e.g., "R U R' U'").

    Args:
        algorithm (str): The algorithm to perform, as a space-separated string of moves.
    """
    moves = algorithm.split()
    for move in moves:
        perform_rotation(move)
    print("\n-----Algorithm completed-----\n")

def close_connections() -> None:
    """
    Close the serial connections to the Arduinos.

    This should be called when communication is finished to free system resources.
    """
    ARDUINO1.close()
    ARDUINO2.close()
