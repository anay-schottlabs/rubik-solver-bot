import time
import board
from digitalio import DigitalInOut, Direction
from microcontroller import Pin
from enum import Enum, auto

class TMC2209:
    """
    Class to control a stepper motor driver (TMC2209) using step and direction pins.
    """

    def __init__(self, step_pin: Pin, dir_pin: Pin, step_degrees: float = 1.8) -> None:
        """
        Initialize the TMC2209 stepper driver with step and direction pins.

        Args:
            step_pin (Pin): The microcontroller pin connected to the STEP input.
            dir_pin (Pin): The microcontroller pin connected to the DIR input.
            step_degrees (float, optional): Degrees per step of the motor. Default is 1.8 degrees.
        """
        self.step_pin = DigitalInOut(step_pin)
        self.dir_pin = DigitalInOut(dir_pin)
        self.step_pin.direction = Direction.OUTPUT  # Set step pin as output
        self.dir_pin.direction = Direction.OUTPUT   # Set direction pin as output

    class MotorDirection(Enum):
        """
        Enum to represent the direction of the stepper motor.
        """
        CLOCKWISE = auto()
        COUNTERCLOCKWISE = auto()

    def move_steps(self, direction: MotorDirection, steps: int, delay: float = 0.001) -> None:
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

class RubikCubeController:
    """
    Class to control a Rubik's Cube using a stepper motor.
    """

    def __init__(self,
                 f_motor: TMC2209,
                 b_motor: TMC2209,
                 r_motor: TMC2209,
                 l_motor: TMC2209,
                 u_motor: TMC2209,
                 d_motor: TMC2209,
                 alg_move_delay: float) -> None:
      """
      Initialize the Rubik's Cube controller with six stepper motors.

      Args:
          f_motor (TMC2209): Stepper motor for the front face.
          b_motor (TMC2209): Stepper motor for the back face.
          r_motor (TMC2209): Stepper motor for the right face.
          l_motor (TMC2209): Stepper motor for the left face.
          u_motor (TMC2209): Stepper motor for the upper face.
          d_motor (TMC2209): Stepper motor for the down face.
          alg_move_delay (float): Delay between moves in the algorithm execution.
      """
      self.motors = {
          'F': f_motor,
          'B': b_motor,
          'R': r_motor,
          'L': l_motor,
          'U': u_motor,
          'D': d_motor
      }
    
    class Face(Enum):
      """
      Enum to represent the faces of the Rubik's Cube.
      """
      FRONT = 'F'
      BACK = 'B'
      RIGHT = 'R'
      LEFT = 'L'
      UP = 'U'
      DOWN = 'D'
  	
    def rotate_face(self, face: Face, direction: TMC2209.MotorDirection, rotations: int = 1) -> None:
      """
      Rotate a specified face of the Rubik's Cube.

      Args:
          face (RubikCubeController.Face): The face to rotate.
          direction (TMC2209.MotorDirection): Direction to rotate the face (CLOCKWISE or COUNTERCLOCKWISE).
          rotations (int, optional): Number of 90 degree rotations to complete, default is 1.
      Raises:
          ValueError: If an invalid face is provided.
      """
      if face not in self.motors:
        raise ValueError("Invalid face")
      
      # find the motor associated with the face
      motor = self.motors.get(face.value)
      
      # have to convert rotations into steps
      steps = rotations * (90 // motor.step_degrees) # make sure to use the motor's step degrees to calculate steps

      # move the motor in the specified direction
      motor.move_steps(direction=direction, steps=steps) # uses the default delay of 0.001 seconds
    
    def algorithm(self, alg_string) -> None:
        """
        Execute a sequence of moves based on an algorithm string using standard Rubik's Cube notation.

        The algorithm string should consist of moves separated by spaces. Each move uses standard cube notation:
          - Faces: F (Front), B (Back), R (Right), L (Left), U (Up), D (Down)
          - A move letter alone (e.g., 'F') means a 90° clockwise turn of that face.
          - A move followed by a prime (e.g., "F'") means a 90° counterclockwise turn (prime move).
          - A move followed by '2' (e.g., 'F2') means a 180° turn (two 90° turns in the same direction).
        
        Examples:
            "R U R' U'"  # Right, Up, Right prime, Up prime
            "F2 D2"      # Front face 180°, Down face 180°
            "L' B2"      # Left face counterclockwise, Back face 180°
        
        Args:
            alg_string (str): A string representing the algorithm to execute, using standard cube notation.
        """
        # Split the algorithm string into individual moves
        moves = alg_string.split()
        
        # Iterate through each move in the algorithm
        for move in moves:
          # determine which face is being moved
          face_letter = move[0].upper()
          # determine if we're doing 1 or 2 rotations
          rotations = 2 if "2" in move else 1
          # determine if the move is prime (counterclockwise) or not (clockwise)
          direction = TMC2209.MotorDirection.COUNTERCLOCKWISE if "'" in move else TMC2209.MotorDirection.CLOCKWISE
          # Get face enum
          try:
            face = self.Face(face_letter)
          except ValueError:
            raise ValueError(f"Invalid face notation: {face_letter}")
          # Rotate the face
          self.rotate_face(face=face, direction=direction, rotations=rotations)
          # small delay for safety
          time.sleep(self.alg_move_delay)

# Define TMC2209 motors with their step and direction pins

# a quick test if this program is run on its own
# note that this program is intended to be a module for main.py
if __name__ == "__main__":
    # rotate a few faces individually

    # run a simple algorithm a few times

    pass
