import cv2
from cv2.gapi import bilateralFilter
import numpy as np
import imutils

IMG_SIZE = (800, 800)
MIN_WIDTH_PLATE_TO_IMAGE_RATIO = 0.3
PLATE_ASPECT_RATIO = 520 / 114


def get_license_plate(image: np.ndarray) -> np.ndarray:
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    bilateral = cv2.bilateralFilter(grey, 5, 50, 50)
    canny = cv2.Canny(bilateral, 20, 60)
    contours = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        width_plate_to_image_ratio = w / image.shape[1]
        if width_plate_to_image_ratio > MIN_WIDTH_PLATE_TO_IMAGE_RATIO:
            peri = cv2.arcLength(contour, True)
            corners = cv2.approxPolyDP(contour, 0.02 * peri, True)
            corners = sorted(corners, key=lambda x: x[0][0])
            if len(corners) != 4:
                continue

            cv2.circle(image, tuple(corners[0][0]), 5, (0, 255, 0), -1)
            cv2.circle(image, tuple(corners[1][0]), 5, (0, 0, 255), -1)
            cv2.circle(image, tuple(corners[2][0]), 5, (255, 0, 0), -1)
            cv2.circle(image, tuple(corners[3][0]), 5, (255, 255, 0), -1)

            # accept only with proper aspect ratio (add to list and later decide)
            license_plate = image[y : y + h, x : x + w]
            return license_plate

    return None


def perform_processing(image: np.ndarray) -> str:
    image = cv2.resize(image, IMG_SIZE)
    # cropped = image[200:600, :] # Kinda cheating lol
    license_plate = get_license_plate(image)

    if license_plate is None:
        return "NOLICENSE"

    cv2.imshow("image", license_plate)
    cv2.waitKey(0)

    return "PO12345"
