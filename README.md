# License Plate Recognition

1. License Plate Detection
    * Find the x-position of the blue vertical rectangle using a mask in the HSV color space.
    * Extract the white elements using a mask in the HSV color space.
    * Sort the white elements based on their area and select the ten largest ones.
    * Accept the first white element that meets the conditions of area, x-position, and number of corners.
    * Perform a perspective transformation on the selected element.

2. Character Recognition
    * Use adaptive thresholding.
    * Sort the found contours based on their area and select the ten largest ones.
    * Sort the contours based on their x-position.
    * Extract individual characters from the image.
    * Compare the extracted characters with the template and select the one with the highest correlation.
    * Add the detected characters to the list.
