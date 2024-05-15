import cv2
import numpy as np
import os

def nothing(x):
    pass

def rgb_to_hsl(image):
    # Convert the image from RGB to HSL
    image = image / 255.0
    hsl_img = np.zeros_like(image, dtype=np.float32)
    r, g, b = image[:, :, 0], image[:, :, 1], image[:, :, 2]

    maxc = np.max(image, axis=2)
    minc = np.min(image, axis=2)
    l = (minc + maxc) / 2.0

    s = np.zeros_like(l)
    h = np.zeros_like(l)

    mask = maxc != minc
    s[mask] = (maxc[mask] - minc[mask]) / (1 - np.abs(2 * l[mask] - 1))

    mask = r == maxc
    h[mask] = (g[mask] - b[mask]) / (maxc[mask] - minc[mask])

    mask = g == maxc
    h[mask] = 2.0 + (b[mask] - r[mask]) / (maxc[mask] - minc[mask])

    mask = b == maxc
    h[mask] = 4.0 + (r[mask] - g[mask]) / (maxc[mask] - minc[mask])

    h = (h / 6.0) % 1.0

    hsl_img[:, :, 0] = h * 179.0  # H channel
    hsl_img[:, :, 1] = s * 255.0  # S channel
    hsl_img[:, :, 2] = l * 255.0  # L channel

    return hsl_img.astype(np.uint8)

def hsl_conversion(img, lower, upper):
    # Convert image to HSL
    hsl_img = rgb_to_hsl(img)

    # Create a mask using the lower and upper bounds
    mask = cv2.inRange(hsl_img, lower, upper)

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

    # Create trackbars for H, S, and L channels
    cv2.createTrackbar('H lower', 'image', 0, 179, nothing)
    cv2.createTrackbar('S lower', 'image', 0, 255, nothing)
    cv2.createTrackbar('L lower', 'image', 0, 255, nothing)
    cv2.createTrackbar('H upper', 'image', 0, 179, nothing)
    cv2.createTrackbar('S upper', 'image', 0, 255, nothing)
    cv2.createTrackbar('L upper', 'image', 0, 255, nothing)

    # Initial values for lower and upper bounds
    lower = np.array([0, 0, 0])
    upper = np.array([179, 255, 255])

    while True:
        # Get current positions of all trackbars
        lower[0] = cv2.getTrackbarPos('H lower', 'image')
        lower[1] = cv2.getTrackbarPos('S lower', 'image')
        lower[2] = cv2.getTrackbarPos('L lower', 'image')
        upper[0] = cv2.getTrackbarPos('H upper', 'image')
        upper[1] = cv2.getTrackbarPos('S upper', 'image')
        upper[2] = cv2.getTrackbarPos('L upper', 'image')

        # Perform HSL conversion
        result = hsl_conversion(img, lower, upper)

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

