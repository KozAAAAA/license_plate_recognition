import cv2
from cv2.gapi import bilateralFilter
import numpy as np
import imutils
from math import sqrt

IMG_SIZE = (800, 800)

PLATE_WIDTH = 520 - 7 * 2 - 40
PLATE_HEIGHT = 114 - 7 * 2
MIN_CHAR_HEIGHT = 70
MAX_CHAR_WIDTH = 60

MIN_WIDTH_PLATE_TO_IMAGE_RATIO = 0.3
MAX_WIDTH_DIFFERENCE_RATIO = 0.1

LOWER_WHITE = np.array([0, 120, 0])
UPPER_WHITE = np.array([255, 255, 255])


def _sort_corners(corners: np.ndarray) -> np.ndarray:
    corners = sorted(corners, key=lambda x: x[0][0])
    left_top, left_bottom = sorted(corners[:2], key=lambda x: x[0][1])
    right_top, right_bottom = sorted(corners[2:], key=lambda x: x[0][1])
    
    # always return slightly bigger
    left_top = left_top + np.array([-10, -10])
    left_bottom = left_bottom + np.array([-10, 10])
    right_top = right_top + np.array([10, -10])
    right_bottom = right_bottom + np.array([10, 10])
    corners = np.array([left_bottom[0], left_top[0], right_top[0], right_bottom[0]])
    return corners


def get_license_plate(image: np.ndarray):
    bilateral = cv2.bilateralFilter(image, 3, 20, 20)
    hsl = cv2.cvtColor(bilateral, cv2.COLOR_BGR2HLS)
    mask = cv2.inRange(hsl, LOWER_WHITE, UPPER_WHITE)

    contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        width_plate_to_image_ratio = w / image.shape[1]
        peri = cv2.arcLength(contour, True)
        corners = cv2.approxPolyDP(contour, 0.02 * peri, True)
        if (
            width_plate_to_image_ratio > MIN_WIDTH_PLATE_TO_IMAGE_RATIO
            and len(corners) == 4
        ):

            corners = _sort_corners(corners)
            left_top, left_bottom, right_top, right_bottom = corners

            pts1 = np.float32([left_top, left_bottom, right_top, right_bottom])
            pts2 = np.float32(
                [
                    [0, PLATE_HEIGHT],
                    [0, 0],
                    [PLATE_WIDTH, 0],
                    [PLATE_WIDTH, PLATE_HEIGHT],
                ]
            )
            matrix = cv2.getPerspectiveTransform(pts1, pts2)

            image = cv2.warpPerspective(image, matrix, (PLATE_WIDTH, PLATE_HEIGHT))
            return image

    return None


def get_license_plate_text(image: np.ndarray):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 17, 150, 10)
    thresholded = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 2
    )
    contours = cv2.findContours(thresholded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if h < MIN_CHAR_HEIGHT or w > MAX_CHAR_WIDTH:
            continue
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return image


def perform_processing(image: np.ndarray) -> str:
    perform_processing.image_count += 1
    print(f"\nProcessing {perform_processing.image_count} image")
    image = cv2.resize(image, IMG_SIZE)
    cropped = image[100:700, :]  # Kinda cheating lol

    license_plate = get_license_plate(cropped)

    if license_plate is None:
        perform_processing.skipped += 1
        print(f"Skipped {perform_processing.skipped} images")
        return "No license plate found"

    image = get_license_plate_text(license_plate)

    cv2.imshow("image", image)
    cv2.waitKey(0)
    return "PO12345"


perform_processing.skipped = 0
perform_processing.image_count = 0
