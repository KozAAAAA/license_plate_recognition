import cv2
import numpy as np
import os

def nothing(x):
    pass

def hsv_conversion(img, lower, upper):
    # Convert image to HSV
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Create a mask using the lower and upper bounds
    mask = cv2.inRange(hsv_img, lower, upper)

    # Apply the mask to the original image
    result = cv2.bitwise_and(img, img, mask=mask)

    return result

def switch_image():
    global current_image_index, image_paths, img
    current_image_index = (current_image_index + 1) % len(image_paths)
    img = cv2.imread(image_paths[current_image_index])
    img = cv2.resize(img, (640, 640))

def main():
    global current_image_index, image_paths, img
    current_image_index = 0
    image_dir = 'data/images/'
    image_paths = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]

    # Load first image
    img = cv2.imread(image_paths[current_image_index])
    img = cv2.resize(img, (640, 640))
    # Create a window
    cv2.namedWindow('image')

    # Create trackbars for H, S, and V channels
    cv2.createTrackbar('H lower', 'image', 0, 179, nothing)
    cv2.createTrackbar('S lower', 'image', 0, 255, nothing)
    cv2.createTrackbar('V lower', 'image', 0, 255, nothing)
    cv2.createTrackbar('H upper', 'image', 0, 179, nothing)
    cv2.createTrackbar('S upper', 'image', 0, 255, nothing)
    cv2.createTrackbar('V upper', 'image', 0, 255, nothing)

    # Initial values for lower and upper bounds
    lower = np.array([0, 0, 0])
    upper = np.array([179, 255, 255])

    while True:
        # Get current positions of all trackbars
        lower[0] = cv2.getTrackbarPos('H lower', 'image')
        lower[1] = cv2.getTrackbarPos('S lower', 'image')
        lower[2] = cv2.getTrackbarPos('V lower', 'image')
        upper[0] = cv2.getTrackbarPos('H upper', 'image')
        upper[1] = cv2.getTrackbarPos('S upper', 'image')
        upper[2] = cv2.getTrackbarPos('V upper', 'image')

        # Perform HSV conversion
        result = hsv_conversion(img, lower, upper)

        # Display result
        cv2.imshow('image', result)

        # Check for key press
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key != 255:  # Check if any key other than 'q' was pressed
            switch_image()

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

