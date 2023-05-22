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
    for face_path in faces_paths:
        face = load_cube_face_image(face_path)
        matches = getFaceShape(face)
        points = getFaceVertices(matches)
        cube_face_img = deleteImageOutline(face, points, width)
        cube_faces.append(getColorsFromCubeFace(cube_face_img))

    sortFaces(cube_faces)
    return Cube(cube_faces)

if __name__ == '__main__':
    listFaces = [
        ROOT_DRIVE + '/cube-0/face0.jpg',
        ROOT_DRIVE + '/cube-0/face1.jpg',
        ROOT_DRIVE + '/cube-0/face2.jpg',
        ROOT_DRIVE + '/cube-0/face3.jpg',
        ROOT_DRIVE + '/cube-0/face4.jpg',
        ROOT_DRIVE + '/cube-0/face5.jpg',
    ]

    cube = load_cube_faces(listFaces)
    print(cube)
