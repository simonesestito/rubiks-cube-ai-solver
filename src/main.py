import os
import cv2
from cube import Cube

from color_extractor import *

ROOT_DRIVE = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", "assets", "images")

def load_cube_face_image(image_path):
    original_image = cv2.imread(image_path)
    width = 100
    height = int(original_image.shape[0]*width/original_image.shape[1])
    return cv2.resize(
        original_image,
        (width, height)
    )


def load_cube_faces(faces_paths, width=100):
    assert len(faces_paths) == 6, "The cube has 6 faces: " + \
        str(len(faces_paths)) + " were given"

    cube_faces = []
    for i, face_path in enumerate(faces_paths):
        print('Loading face', i)
        face = load_cube_face_image(face_path)
        matches = getFaceShape(face)
        points = getFaceVertices(matches)
        cube_face_img = deleteImageOutline(face, points, width)
        cube_faces.append(getColorsFromCubeFace(cube_face_img))

    sortFaces(cube_faces)
    return Cube(cube_faces)

if __name__ == '__main__':
    import sys
    from cubes_map import CubesMap

    cubes_map = CubesMap() # ONLY ONE INSTANCE!! It is super heavy

    while True:
        rootCube = input('Cube: ')
        print('Loading cube', rootCube)

        # Files in rootCube folder
        listFaces = [
            os.path.join(ROOT_DRIVE, rootCube, f)
            for f in os.listdir(os.path.join(ROOT_DRIVE, rootCube))
            if os.path.isfile(os.path.join(ROOT_DRIVE, rootCube, f))
        ]
        print(listFaces)
        assert len(listFaces) == 6, "The cube must have 6 faces (= 6 photos in the folder)"

        cube = load_cube_faces(listFaces)
        print(cube)
    

        # Solve
        while not cube.is_solved():
            next_move = cubes_map[cube]
            if next_move is None:
                print('ERROR: Cube is not known! Photos may be wrong, or the cube needs more than 8 moves to be solved.')
                break
            print('Next move:', next_move)
            cube.perform_action(next_move)
            print(cube)

        print('='*50)
