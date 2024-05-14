import cv2
from cv2.gapi import bilateralFilter
import numpy as np
import imutils

IMG_SIZE = (800, 800)
MIN_WIDTH_PLATE_TO_IMAGE_RATIO = 0.3
PLATE_ASPECT_RATIO = 520 / 114
LOWER_WHITE = np.array([0, 120, 0])
UPPER_WHITE = np.array([255, 255, 255])

def _sort_corners(corners: np.ndarray) -> np.ndarray:
    corners = sorted(corners, key=lambda x: x[0][0])
    left_top, left_bottom = sorted(corners[:2], key=lambda x: x[0][1])
    right_top, right_bottom = sorted(corners[2:], key=lambda x: x[0][1])
    corners = np.array([left_bottom[0], left_top[0], right_top[0], right_bottom[0]])
    return corners

def get_license_plate(image: np.ndarray) -> np.ndarray:
    bilateral = cv2.bilateralFilter(image, 3, 20, 20)
    hsl = cv2.cvtColor(bilateral, cv2.COLOR_BGR2HLS)
    mask = cv2.inRange(hsl, LOWER_WHITE, UPPER_WHITE)
    
    # return mask

    contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    
    # return eroded
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        width_plate_to_image_ratio = w / image.shape[1]
        peri = cv2.arcLength(contour, True)
        corners = cv2.approxPolyDP(contour, 0.02 * peri, True)
        if width_plate_to_image_ratio > MIN_WIDTH_PLATE_TO_IMAGE_RATIO and len(corners) == 4:
            
            corners = _sort_corners(corners)
            left_top, left_bottom, right_top, right_bottom = corners
            cv2.circle(image, left_top, 5, (0, 255, 0), -1)
            cv2.circle(image, left_bottom, 5, (0, 0, 255), -1)
            cv2.circle(image, right_top, 5, (255, 0, 0), -1)
            cv2.circle(image, right_bottom, 5, (255, 255, 0), -1)

            # accept only with proper aspect ratio (add to list and later decide)
            license_plate = image[y : y + h, x : x + w]
            return license_plate
    
    return None



def perform_processing(image: np.ndarray) -> str:
    perform_processing.image_count += 1
    print(f"\nProcessing {perform_processing.image_count} image")
    image = cv2.resize(image, IMG_SIZE)
    cropped = image[100:700, :] # Kinda cheating lol
    license_plate = get_license_plate(cropped)
    if license_plate is None:
        perform_processing.skipped += 1
        print(f"Skipped {perform_processing.skipped} images")
        return "No license plate found"

    cv2.imshow("image", license_plate)
    cv2.waitKey(0)
    return "PO12345"
perform_processing.skipped = 0
perform_processing.image_count = 0
