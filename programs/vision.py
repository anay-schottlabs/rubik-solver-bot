from cv2 import VideoCapture
from cv2.typing import MatLike
from math import dist
from arduino_comm import perform_algorithm

# the pixel locations on the image where cube piece colors are located
# center pieces are omitted since they are covered by the rotating shafts
image_points = [
    [235,111], # 0, up face
    [359,147], # 1, up face
    [439,205], # 2, up face
    [368,253], # 3, up face
    [291,313], # 4, up face
    [208,262], # 5, up face
    [128,206], # 6, up face
    [200,152], # 7, up face

    [95,281],  # 8, left face
    [173,322], # 9, left face
    [248,371], # 10, left face
    [250,452], # 11, left face
    [220,476], # 12, left face
    [187,474], # 13, left face
    [94,392],  # 14, left face
    [100,351], # 15, left face

    [329,382], # 16, front face
    [401,316], # 17, front face
    [469,272], # 18, front face
    [472,337], # 19, front face
    [479,389], # 20, front face
    [394,471], # 21, front face
    [351,476], # 22, front face
    [328,453]  # 23, front face
]

# stuff for dealing with the cube state mapping
DEFAULT_CUBE_STR = "XXXXUXXXXXXXXRXXXXXXXXFXXXXXXXXDXXXXXXXXLXXXXXXXXBXXXX" # X is just a placeholder for unknown colors, centers are already defined
PIECE_ORDER = [                         # this makes it much easier to find the index of a piece in the cube state string
    "U1", "U2", "U3", "U4", "U5", "U6", "U7", "U8", "U9", # up face
    "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", # right face
    "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", # front face
    "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", # down face
    "L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8", "L9", # left face
    "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9" # back face
]
COLORS = {                 # rgb color that roughly corresponds to the cube piece colors
    (209, 190, 183): "U",  # up face, white
    (255, 128, 0): "R",    # right face, orange
    (24, 29, 61): "F",     # front face, blue
    (255, 255, 0): "D",    # down face, yellow
    (219, 101, 106): "L",  # left face, red
    (0, 255, 0): "B"       # back face, green
}
DEFAULT_MAPPING = ["U3", "U6", "U9", "U8", "U7", "U4", "U1", "U2",
                   "L1", "L2", "L3", "L6", "L9", "L8", "L7", "L4",
                   "F1", "F2", "F3", "F6", "F9", "F8", "F7", "F4"]
FB_MAPPING = ["D7", "X", "D1", "D2", "D3", "X", "D9", "D8",
              "R9", "X", "R7", "R4", "R1", "X", "R3", "R6",
              "X", "X", "X", "X", "X", "X", "X", "X"]
LR_MAPPING = ["X", "D6", "X", "X", "X", "D4", "X", "X",
              "X", "X", "X", "X", "X", "X", "X", "X",
              "B9", "X", "B7", "B4", "B1", "X", "B3", "B6"]
UD_MAPPING = ["X", "X", "X", "X", "X", "X", "X", "X",
              "X", "R2", "X", "X", "X", "R8", "X", "X",
              "X", "B2", "X", "x", "x", "B8", "X", "X"]

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

def get_image_point_colors(image: MatLike) -> list[str]:
    """
    Extract the colors of the cube pieces from the captured image based on predefined pixel locations.

    Args:
        image (MatLike): The captured image frame containing the Rubik's Cube.

    Returns:
        list[str]: A list of colors corresponding to the cube piece locations.
    """
    three_face_colors = [] # list that will hold the colors of the three visible faces of the cube

    # iterate through the predefined pixel locations and extract the colors
    for point in image_points:

        bgr = image[point[1], point[0]] # extract the colors, but they're in BGR format (takes [y, x] format)
        rgb = (bgr[2], bgr[1], bgr[0]) # convert bgr to rgb format

        color_dists = []
        # calculate the euclidean distance between the piece's rgb value and each of the predefined colors
        # the lowest euclidean distance will correspond to the closest color
        for color in list(COLORS.keys()):
            color_dists.append(dist(rgb, color)) # calculate the distance
        
        closest_color_index = color_dists.index(min(color_dists)) # find the index of the closest color
        closest_face = list(COLORS.values())[closest_color_index] # use that index to find the corresponding face (U, R, F, D, L, B)

        three_face_colors.append(closest_face)

    return three_face_colors

def map_faces_to_cube_state(cube_state: str, three_face_colors: list[str], mapping: list[str]) -> str:
    """
    Map the colors of the three visible faces to the cube state string.

    Args:
        cube_state (str): The current cube state string.
        three_face_colors (list[str]): The list of colors for the three visible faces.
        mapping (list[str]): The piece order for the visible faces, will change when cube is rotated.

    Returns:
        str: The updated cube state string with the mapped colors.
    """
    cube_state = list(cube_state) # convert the cube state string to a list for easier manipulation

    for i, face in enumerate(three_face_colors):
        # after rotating, some pieces will not change, so just skip them
        # these will be notated in the mapping as "X"
        if mapping[i] not in PIECE_ORDER:
            continue

        piece = mapping[i]               # find what piece this is
        index = PIECE_ORDER.index(piece) # find the index of that piece in the cube state string
        cube_state[index] = face         # populate the cube state string with the color of the piece
    
    return "".join(cube_state) # join the list back int oa string and return it

def get_cube_state() -> str:
    """
    Capture images of the Rubik's Cube in different orientations and reconstruct its full state.

    This function performs the following steps:
      1. Captures an image of the default cube orientation and maps the visible pieces.
      2. Rotates the F and B faces 180° to expose the down and right faces, captures an image, maps the new visible pieces, then resets orientation.
      3. Rotates the L and R faces 180° to expose the down and back faces, captures an image, maps the new visible pieces, then resets orientation.
      4. Rotates the U and D faces 180° to expose the right and back faces, captures an image, maps the new visible pieces, then resets orientation.
      5. Combines all detected colors into a single cube state string in standard piece order.

    The function uses predefined pixel locations and color mappings to identify each piece's color.
    It communicates with the robot to rotate the cube as needed and updates the cube state after each image.

    Returns:
        str: A string representing the detected cube state, with each character corresponding to a piece color in PIECE_ORDER.
    """
    camera = VideoCapture(0)  # Open the default camera

    cube_state = DEFAULT_CUBE_STR  # Start with the default cube state string

    # 1. Capture the default orientation, then populate cube state
    default_pic = take_picture(camera=camera)
    colors = get_image_point_colors(image=default_pic)  # Get the colors of the three visible faces
    cube_state = map_faces_to_cube_state(cube_state=cube_state, three_face_colors=colors, mapping=DEFAULT_MAPPING)  # Map the colors to the cube state

    # 2. Rotate F and B faces to reveal the back, capture, then reset and populate cube state
    perform_algorithm("F2 B2")

    fb_pic = take_picture(camera=camera)
    colors = get_image_point_colors(image=fb_pic)  # Get the colors of the new pieces after rotation
    cube_state = map_faces_to_cube_state(cube_state=cube_state, three_face_colors=colors, mapping=FB_MAPPING)  # Map the colors to the cube state

    perform_algorithm("F2 B2") # reset the cube to the default orientation

    # 3. Rotate L and R faces to reveal the back, capture, then reset and populate cube state
    perform_algorithm("L2 R2")

    lr_pic = take_picture(camera=camera)
    colors = get_image_point_colors(image=lr_pic)  # Get the colors of the new pieces after rotation
    cube_state = map_faces_to_cube_state(cube_state=cube_state, three_face_colors=colors, mapping=LR_MAPPING)  # Map the colors to the cube state

    perform_algorithm("L2 R2") # reset the cube to the default orientation

    # 4. Rotate U and D faces to reveal the back, capture, then reset and populate cube state
    perform_algorithm("U2 D2")

    ud_pic = take_picture(camera=camera)
    colors = get_image_point_colors(image=ud_pic)  # Get the colors of the new pieces after rotation
    cube_state = map_faces_to_cube_state(cube_state=cube_state, three_face_colors=colors, mapping=UD_MAPPING)  # Map the colors to the cube state

    perform_algorithm("U2 D2") # reset the cube to the default orientation

    camera.release()  # Release the camera resource

    return cube_state  # Return the fully populated cube state string

if __name__ == "__main__":
    # If run directly, print the detected (placeholder) cube state
    print(get_cube_state())
