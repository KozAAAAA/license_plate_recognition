import cv2
import numpy as np
import imutils

from processing.config import Image, Plate
from processing.license_plate import get_license_plate
from processing.ocr import get_text


def perform_processing(image: np.ndarray) -> str:
    perform_processing.image_number += 1
    print(f"Processing image {perform_processing.image_number}")
    image = cv2.resize(image, (Image.WIDTH, Image.HEIGHT))
    license_plate = get_license_plate(image)

    if license_plate is None:
        perform_processing.skipped += 1
        print(f"Skipped {perform_processing.skipped} images")
        return "PO777777"

    text = get_text(license_plate)
    if not text:
        return "PO777777"
    
    return text


perform_processing.skipped = 0
perform_processing.image_number = 0
