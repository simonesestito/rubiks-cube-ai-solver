import numpy
import cv2
from cube import Cube

from color_extractor import *

ROOT_DRIVE = '/mnt/c/Users/SABRINA/Downloads/'

def loadCubeFaceImage(imagePath):
    originalImage = cv2.imread(imagePath)
    width = 100
    height =int(originalImage.shape[0]*width/originalImage.shape[1])
    return cv2.resize(
        originalImage,
        (width,height)
    )

def loadCubeFaces(facesPath):
    assert len(facesPath) == 6, "The cube has 6 faces: " + str(len(facesPath)) + " were given"

    facesCube = []
    for facePath in listFaces:
        face = loadCubeFaceImage(facePath)
        matches = getFaceShape(face)
        points = getFaceVertices(matches)
        cubeFaceImg = deleteImageOutline(face, points, width)
        facesCube.append(getColorsFromCubeFace(cubeFaceImg))

    sortFaces(facesCube)
    return Cube(facesCube)

if __name__ == '__main__':
    listFaces = [
        ROOT_DRIVE + 'cube-faces/face1.jpg',
        ROOT_DRIVE + 'cube-faces/face2.jpg',
        ROOT_DRIVE + 'cube-faces/face3.jpg',
        ROOT_DRIVE + 'cube-faces/face4.jpg',
        ROOT_DRIVE + 'cube-faces/face5.jpg',
        ROOT_DRIVE + 'cube-faces/face6.jpg',
    ]

    cube = loadCubeFaces(listFaces)
    print(cube)