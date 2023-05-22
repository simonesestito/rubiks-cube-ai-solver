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

    rootCube = sys.argv[1] if len(sys.argv) > 1 else 'cube-0'
    listFaces = [
        os.path.join(ROOT_DRIVE, rootCube, 'face0.jpg'),
        os.path.join(ROOT_DRIVE, rootCube, 'face1.jpg'),
        os.path.join(ROOT_DRIVE, rootCube, 'face2.jpg'),
        os.path.join(ROOT_DRIVE, rootCube, 'face3.jpg'),
        os.path.join(ROOT_DRIVE, rootCube, 'face4.jpg'),
        os.path.join(ROOT_DRIVE, rootCube, 'face5.jpg'),
    ]

    cube = load_cube_faces(listFaces)
    print(cube)
