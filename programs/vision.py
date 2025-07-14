from cv2 import VideoCapture
from cv2.typing import MatLike
from arduino_comm import perform_algorithm

def take_picture(camera: VideoCapture) -> MatLike:
    """
    Capture a single image frame from the provided camera.

    Args:
        camera (VideoCapture): The camera object to capture the image from.

    Returns:
        MatLike: The captured image frame.

    Raises:
        RuntimeError: If the image could not be captured.
    """
    ret, frame = camera.read()  # Attempt to capture a frame from the camera
    if not ret:
        raise RuntimeError("Failed to capture image from camera.")
    return frame

def get_cube_state() -> str:
    """
    Capture images of the Rubik's Cube in different orientations to determine its state.

    This placeholder function simulates the vision processing workflow:
      1. Takes a picture of the default cube orientation.
      2. Rotates the F and B faces 180° to reveal the back, takes a picture, then resets.
      3. Rotates the L and R faces 180° to reveal the back, takes a picture, then resets.
    The actual vision processing logic to extract the cube state from images is not implemented yet.

    Returns:
        str: A string representing the detected cube state (currently hardcoded).
    """
    camera = VideoCapture(0)  # Open the default camera

    try:
        # 1. Capture the default orientation
        default_pic = take_picture(camera)

        # 2. Rotate F and B faces to reveal the back, capture, then reset
        perform_algorithm("F2 B2")
        fb_pic = take_picture(camera)
        perform_algorithm("F2 B2")

        # 3. Rotate L and R faces to reveal the back, capture, then reset
        perform_algorithm("L2 R2")
        lr_pic = take_picture(camera)
        perform_algorithm("L2 R2")

    except RuntimeError as e:
        # If there is an error in capturing the image, print the error and return the solved cube state
        print(f"Error: {e}")
        return "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"

    camera.release()  # Release the camera resource

    # TODO: Implement vision processing to analyze captured images and return the actual cube state.
    # For now, return a hardcoded cube state string for testing.
    return "DRLUUBFBRBLURRLRUBLRDDFDLFUFUFFDBRDUBRUFLLFDDBFLUBLRBD"

if __name__ == "__main__":
    # If run directly, print the detected (placeholder) cube state
    print(get_cube_state())
