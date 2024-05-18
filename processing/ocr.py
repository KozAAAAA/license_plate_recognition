import cv2
import numpy as np
import os
import imutils

from processing.config import Char, FONT_CHARS_PATH


def get_list_of_chars(image: np.ndarray, contours) -> np.ndarray:
    chars = []
    contours = sorted(contours, key=lambda contour: cv2.boundingRect(contour)[0])
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if h < Char.MIN_HEIGHT or w > Char.MAX_WIDTH:
            continue
        char = image[y : y + h, x : x + w]
        char = cv2.resize(char, (Char.WIDTH, Char.HEIGHT))
        chars.append(char)

    return np.array(chars)


def get_list_of_font_chars_and_names() -> tuple[np.ndarray, list]:
    font_files = os.listdir(FONT_CHARS_PATH)
    chars = []
    for char in font_files:
        char = cv2.imread(f"{FONT_CHARS_PATH}/{char}", cv2.IMREAD_GRAYSCALE)
        thresh_char = cv2.threshold(char, 128, 255, cv2.THRESH_BINARY_INV)[1]
        contours, _ = cv2.findContours(
            thresh_char, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
        x, y, w, h = cv2.boundingRect(contours[0])
        char = char[y : y + h, x : x + w]
        char = cv2.resize(char, (Char.WIDTH, Char.HEIGHT))
        chars.append(char)
    return np.array(chars), [os.path.splitext(char)[0] for char in font_files]


def get_text(image: np.ndarray) -> str:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 17, 150, 10)
    thresholded = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 2
    )
    contours = cv2.findContours(thresholded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    chars = get_list_of_chars(thresholded, contours)
    font_chars, font_char_names = get_list_of_font_chars_and_names()

    text = ""
    for char in chars:
        probs = []
        for font_char in font_chars:
            res = cv2.matchTemplate(char, font_char, cv2.TM_CCOEFF_NORMED)
            probs.append(np.max(res))
        text += font_char_names[np.argmax(probs)]

    return text
