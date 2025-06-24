import time
import board
from digitalio import DigitalInOut, Direction as DioDirection
from microcontroller import Pin
from enum import Enum, auto

class TMC2209:
    """
    Class to control a stepper motor driver (TMC2209) using step and direction pins.
    """

    def __init__(self, step_pin: Pin, dir_pin: Pin) -> None:
        """
        Initialize the TMC2209 stepper driver with step and direction pins.

        Args:
            step_pin (Pin): The microcontroller pin connected to the STEP input.
            dir_pin (Pin): The microcontroller pin connected to the DIR input.
        """
        self.step_pin = DigitalInOut(step_pin)
        self.dir_pin = DigitalInOut(dir_pin)
        self.step_pin.direction = DioDirection.OUTPUT  # Set step pin as output
        self.dir_pin.direction = DioDirection.OUTPUT   # Set direction pin as output

    class Direction(Enum):
        """
        Enum to represent the direction of the stepper motor.
        """
        CLOCKWISE = auto()
        COUNTERCLOCKWISE = auto()

    def move_steps(self, direction: 'TMC2209.Direction', steps: int, delay: float = 0.001) -> None:
        """
        Move the stepper motor a specified number of steps in the given direction.

        Args:
            direction (TMC2209.Direction): Direction to move the motor (CLOCKWISE or COUNTERCLOCKWISE).
            steps (int): Number of steps to move.
            delay (float, optional): Delay between steps in seconds. Default is 0.001.
        Raises:
            ValueError: If an invalid direction is provided.
        """
        # Set the direction pin based on the desired direction
        if direction == self.Direction.CLOCKWISE:
            self.dir_pin.value = True
        elif direction == self.Direction.COUNTERCLOCKWISE:
            self.dir_pin.value = False
        else:
            raise ValueError("Invalid direction")

        # Pulse the step pin for the specified number of steps
        for _ in range(steps):
            self.step_pin.value = True   # Step pin HIGH
            time.sleep(delay)            # Wait for the step to register
            self.step_pin.value = False  # Step pin LOW
            time.sleep(delay)            # Wait before next