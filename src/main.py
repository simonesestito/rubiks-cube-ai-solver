import numpy
import cv2
from cube import Cube

from color_extractor import *

ROOT_DRIVE = '/mnt/c/Users/SABRINA/Downloads/'

origin = cv2.imread(ROOT_DRIVE+"faccia1.jpeg")
width = 100
height =int(origin.shape[0]*width/origin.shape[1])
faccia1 = cv2.resize(
    origin,
    (width,height)
)

origin = cv2.imread(ROOT_DRIVE+"faccia2.jpeg")
width = 100
height =int(origin.shape[0]*width/origin.shape[1])
faccia2 = cv2.resize(
    origin,
    (width,height)
)

origin = cv2.imread(ROOT_DRIVE+"faccia3.jpeg")
width = 100
height =int(origin.shape[0]*width/origin.shape[1])
faccia3 = cv2.resize(
    origin,
    (width,height)
)

origin = cv2.imread(ROOT_DRIVE+"faccia4.jpeg")
width = 100
height =int(origin.shape[0]*width/origin.shape[1])
faccia4 = cv2.resize(
    origin,
    (width,height)
)

origin = cv2.imread(ROOT_DRIVE+"faccia5.jpeg")
width = 100
height =int(origin.shape[0]*width/origin.shape[1])
faccia5 = cv2.resize(
    origin,
    (width,height)
)

origin = cv2.imread(ROOT_DRIVE+"faccia6.jpeg")
width = 100
height =int(origin.shape[0]*width/origin.shape[1])
faccia6 = cv2.resize(
    origin,
    (width,height)
)


listFaces = [faccia6, faccia2, faccia3, faccia4, faccia5, faccia1]
facesCube = []
for face in listFaces: 
    matches = getFaceShape(face)
    points = getFaceVertices(matches)
    print(points)
    cube_face_img = deleteImageOutline(face, points, width)
    facesCube.append(getColorsFromCubeFace(cube_face_img))

print(facesCube)

sortFaces(facesCube)

cube = Cube(facesCube)
print(cube)

