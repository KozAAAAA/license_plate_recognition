import numpy as np

MIN_WIDTH_PLATE_TO_IMAGE_RATIO = 0.3
MIN_HEIGHT_PLATE_TO_IMAGE_RATIO = 0.065

class Image:
    WIDTH = 800
    HEIGHT = 800


class Plate:
    WIDTH = 520 - 7 * 2 - 40
    HEIGHT = 114 - 7 * 2

    MIN_AREA = 20000
    MAX_AREA = 90000


class Char:
    MAX_WIDTH = 70
    MIN_HEIGHT = 65


class White:
    LOWER = np.array([0, 0, 150])
    UPPER = np.array([180, 50, 255])


class Blue:
    LOWER = np.array([73, 140, 70])
    UPPER = np.array([113, 255, 255])
