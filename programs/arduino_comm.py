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

# Both arduinos are on 9600 baud with a timeout of 1 second
ARDUINO1 = serial.Serial(ARDUINO1_PORT, 9600, timeout=1)
# ARDUINO2 = serial.Serial(ARDUINO2_PORT, 9600, timeout=1

def perform_rotation(move_notation: str) -> None:
    print(f"Sending {move_notation}")

    while True:
        # Write the move notation to both arduinos
        ARDUINO1.write(move_notation.encode())
        # ARDUINO2.write(move_notation.encode())

        # Read the response from the arduinos
        line1 = ARDUINO1.readline().decode().strip()
        line2 = None# ARDUINO2.readline().decode().strip()

        # Check if the arduinos responded with a valid message
        if line1 == move_notation or line2 == move_notation:
            print(f"Received {line1 if line1 == move_notation else line2}")
            print("Move completed\n")
            break
