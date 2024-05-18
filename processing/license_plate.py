import numpy as np
import cv2
import imutils

from processing.config import Blue, White, Plate


def sort_corners(corners: np.ndarray, offset: int) -> np.ndarray:
    corners = sorted(corners, key=lambda x: x[0][0])
    left_top, left_bottom = sorted(corners[:2], key=lambda x: x[0][1])
    right_top, right_bottom = sorted(corners[2:], key=lambda x: x[0][1])

    left_top = left_top + np.array([-offset, -offset])
    left_bottom = left_bottom + np.array([-offset, offset])
    right_top = right_top + np.array([offset, -offset])
    right_bottom = right_bottom + np.array([offset, offset])
    corners = np.array([left_bottom[0], left_top[0], right_top[0], right_bottom[0]])
    return corners


def get_licence_plate_x(image: np.ndarray):
    """Extract the x coordinate of the license plate base on the blue color"""

    bilateral = cv2.bilateralFilter(image, 3, 50, 50)
    hsv = cv2.cvtColor(bilateral, cv2.COLOR_BGR2HSV)
    mask_blue = cv2.inRange(hsv, Blue.LOWER, Blue.UPPER)

    contours = cv2.findContours(mask_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if h > w:
            return x

    return 0


def get_license_plate(image: np.ndarray):
    min_x = get_licence_plate_x(image)

    bilateral = cv2.bilateralFilter(image, 3, 50, 50)
    hsv = cv2.cvtColor(bilateral, cv2.COLOR_BGR2HSV)
    mask_white = cv2.inRange(hsv, White.LOWER, White.UPPER)

    contours = cv2.findContours(mask_white, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    for contour in contours:
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        peri = cv2.arcLength(contour, True)
        corners = cv2.approxPolyDP(contour, 0.02 * peri, True)

        if Plate.MIN_AREA < area < Plate.MAX_AREA and x > min_x and len(corners) == 4:
            pts1 = np.float32(sort_corners(corners, 10))
            pts2 = np.float32(
                [
                    [0, Plate.HEIGHT],
                    [0, 0],
                    [Plate.WIDTH, 0],
                    [Plate.WIDTH, Plate.HEIGHT],
                ]
            )
            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            image = cv2.warpPerspective(image, matrix, (Plate.WIDTH, Plate.HEIGHT))

            return image

    return None
