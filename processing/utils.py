import cv2
import numpy as np

IMG_SIZE = (640, 640)
LICENCE_PLATE_SIZE = (520, 114)

def perform_processing(image: np.ndarray) -> str:
    image = cv2.resize(image, IMG_SIZE)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image, (5, 5), 0)
    image = cv2.Canny(image, 50, 250)

    # Find licence plate rectangle
    # Extract only the licence plate
    # Resize licence plate based on known proportions
    # Perform some kind of thresholding
    # Detect individual characters based on contours
    # Recognize characters somehow
    # Display
    cv2.imshow('image', image)
    cv2.waitKey(0)

    return 'PO12345'
