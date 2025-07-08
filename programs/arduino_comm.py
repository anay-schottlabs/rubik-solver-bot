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
load_dotenv()

# Determine the serial ports for the arduinos
ARDUINO1_PORT = getenv("ARDUINO1_PORT")
ARDUINO2_PORT = getenv("ARDUINO2_PORT")

# Both arduinos are on 115200 baud, with no timeout
ARDUINO1 = serial.Serial(ARDUINO1_PORT, 115200)
# ARDUINO2 = serial.Serial(ARDUINO2_PORT, 115200)

def perform_rotation(move_notation: str) -> None:
    # \n is added to the end of the messages to indicate the end of the message
    ARDUINO1.write(move_notation.encode() + "\n")
    # ARDUINO2.write(move_notation.encode() + "\n")

	# Read the response from the arduinos
    line1 = ARDUINO1.readline().decode()
    line2 = None# ARDUINO2.readline().decode()

	# Wait for either arduino to echo the move notation back
    while not move_notation == line1 and not move_notation == line2:
        # Keep reading until we get a valid response
        line1 = ARDUINO1.readline().decode()
        # line2 = ARDUINO2.readline().decode()

