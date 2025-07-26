"""
Raspberry Pi 4B Stepper Motor Controller for Rubik's Cube Solver

This script controls six stepper motors connected to the Pi's GPIO pins.
It exposes a method to execute a cube algorithm string using standard notation.
Test usage: Run this script and enter algorithms interactively, just like arduino_comm.py.

Pin assignments (BCM numbering):
    U: step=4,  dir=17
    F: step=27, dir=22
    L: step=5,  dir=6
    D: step=26, dir=23
    B: step=24, dir=25
    R: step=12, dir=16
"""

import time
import RPi.GPIO as GPIO
from enum import Enum

# GPIO pin mapping for each face (step, dir)
FACE_PINS = {
    'U': (4, 17),    # Up face
    'F': (27, 22),   # Front face
    'L': (5, 6),     # Left face
    'D': (26, 23),   # Down face
    'B': (24, 25),   # Back face
    'R': (12, 16)    # Right face
}

class Direction(Enum):
    """
    Enum to represent the direction of stepper motor rotation.
    """
    CLOCKWISE = 1
    COUNTERCLOCKWISE = -1

# Number of steps required for a 90-degree face turn (adjust for your hardware)
STEPS_PER_90 = 50

class StepperMotor:
    """
    Represents a single stepper motor controlled via GPIO pins.
    """
    def __init__(self, step_pin, dir_pin):
        """
        Initialize the stepper motor with step and direction pins.

        Args:
            step_pin (int): GPIO pin for step signal.
            dir_pin (int): GPIO pin for direction signal.
        """
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin, GPIO.OUT)

    def move(self, direction: Direction, steps: int, delay: float = 0.001):
        """
        Move the stepper motor a given number of steps in the specified direction.

        Args:
            direction (Direction): Direction to rotate (CLOCKWISE or COUNTERCLOCKWISE).
            steps (int): Number of steps to move.
            delay (float): Delay between steps in seconds (default 0.001 = 1000 microseconds).
        """
        GPIO.output(self.dir_pin, GPIO.HIGH if direction == Direction.CLOCKWISE else GPIO.LOW)
        for _ in range(steps):
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(delay)

class CubeStepperController:
    """
    Controls all six stepper motors for the Rubik's Cube using GPIO.
    """
    def __init__(self):
        """
        Initialize the controller and all stepper motors.
        """
        GPIO.setmode(GPIO.BCM)
        # Create a StepperMotor instance for each face using the pin mapping
        self.motors = {face: StepperMotor(*FACE_PINS[face]) for face in FACE_PINS}

    def rotate_face(self, face: str, direction: Direction, rotations: int = 1):
        """
        Rotate a cube face by a given number of 90-degree turns.

        Args:
            face (str): Face to rotate ('U', 'F', 'L', 'D', 'B', 'R').
            direction (Direction): Direction to rotate (CLOCKWISE or COUNTERCLOCKWISE).
            rotations (int): Number of 90-degree turns (default 1).
        Raises:
            ValueError: If the face is not valid.
        """
        if face not in self.motors:
            raise ValueError(f"Invalid face: {face}")
        steps = STEPS_PER_90 * rotations
        self.motors[face].move(direction, steps)

    def perform_algorithm(self, algorithm: str):
        """
        Execute a sequence of moves using standard cube notation.

        Steps:
            1. Break up the algorithm string by spaces.
            2. For each move, determine the face.
            3. Determine if the move is prime (contains "'").
            4. Determine if the move is double (contains "2").
            5. Call rotate_face with the correct parameters.
            6. Print a message after each move.
            7. Print a message after the entire algorithm.

        Supports moves like U, U', U2, etc.

        Args:
            algorithm (str): The algorithm string (e.g., "U R' L2 F2' B D2").
        """
        moves = algorithm.split()  # 1. Break up the alg string by spaces
        for move in moves:
            face = move[0].upper()  # 2. Determine the face
            prime = "'" in move      # 3. Determine if the move is prime
            double = "2" in move     # 4. Determine if the move is double
            rotations = 2 if double else 1
            direction = Direction.COUNTERCLOCKWISE if prime else Direction.CLOCKWISE
            self.rotate_face(face, direction, rotations)  # 5. Call rotate_face
            print(f"Completed move: {move}")              # 6. Say completed move
        print(f"----- Completed algorithm: {algorithm} -----")  # 7. Say completed algorithm and what

    def cleanup(self):
        """
        Clean up GPIO resources. Should be called before exiting the program.
        """
        GPIO.cleanup()

if __name__ == "__main__":
    # Interactive loop for testing: enter algorithms until interrupted
    controller = CubeStepperController()
    try:
        while True:
            alg_str = input("Enter an algorithm (example: U R' L2 F2' B D2): ")
            controller.perform_algorithm(alg_str)
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    finally:
        print("Cleaning up...")
        controller.cleanup()