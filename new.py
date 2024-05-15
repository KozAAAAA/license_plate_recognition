import cv2 as cv
import numpy as np

from pathlib import Path


def empty_callback(value):
    pass


cv.namedWindow('image')

cv.createTrackbar('hue_l', 'image', 0, 180, empty_callback)
cv.createTrackbar('hue_h', 'image', 180, 180, empty_callback)
cv.createTrackbar('sat_l', 'image', 0, 255, empty_callback)
cv.createTrackbar('sat_h', 'image', 50, 255, empty_callback)   
cv.createTrackbar('val_l', 'image', 150, 255, empty_callback)
cv.createTrackbar('val_h', 'image', 255, 255, empty_callback)

cv.createTrackbar('area_min', 'image', 50, 200, empty_callback)     # critical=63, 24 negarives if 50 < area
cv.createTrackbar('area_max', 'image', 180, 200, empty_callback)    # critical=150, 13 negatives if 50 < area < 180

                                                                    # with area conditions applied
cv.createTrackbar('w_min', 'image', 15, 50, empty_callback)         # critical=17, 7 negatives if 14 < w
cv.createTrackbar('w_max', 'image', 35, 50, empty_callback)         # critical=28, 10 negatives if w < 35
cv.createTrackbar('h_min', 'image', 30, 100, empty_callback)        # critical=38, 12 negatives if 30 < h
cv.createTrackbar('h_max', 'image', 75, 100, empty_callback)        # critical=66, 7 negatives if h < 75
                                                                    # 2 negatives for all conditions above from area, w and h

                                                                    # with area conditions applied
cv.createTrackbar('ratio_min', 'image', 25, 100, empty_callback)    # critical=31, 6 negatives if 25 < ratio
cv.createTrackbar('ratio_max', 'image', 75, 100, empty_callback)    # critical=64, 9 negatives if ratio < 75
                                                                    # 1 negative for all conditions above from area, w, h and ratio

                                                                    # with area conditions applied
cv.createTrackbar('extent_min', 'image', 70, 100, empty_callback)   # critical=78, 1 negative if 70 < extent
cv.createTrackbar('solid_min', 'image', 75, 100, empty_callback)    # critical=83, 8 negatives if 75 < solidity
                                                                    # 0 negatives for all conditions above from area, w, h, ratio, extent and solidity


path = Path('./data/images/')
frames = list(sorted(path.iterdir()))
cnt = 0
cnt_max = len(frames)
err = np.zeros(cnt_max)

while True:

    # slideshow control
    key = cv.waitKey(30)
    if key == 27:   # escape key
        break
    elif key == ord('a'):
        cnt -= 1
    elif key == ord('d'):
        cnt += 1
    img = cv.imread(str(frames[cnt % cnt_max]))

    # get trackbar values
    hue_l = cv.getTrackbarPos('hue_l', 'image')
    hue_h = cv.getTrackbarPos('hue_h', 'image')
    sat_l = cv.getTrackbarPos('sat_l', 'image')
    sat_h = cv.getTrackbarPos('sat_h', 'image')
    val_l = cv.getTrackbarPos('val_l', 'image')
    val_h = cv.getTrackbarPos('val_h', 'image')

    area_min = cv.getTrackbarPos('area_min', 'image') * 10000
    area_max = cv.getTrackbarPos('area_max', 'image') * 10000

    w_min = cv.getTrackbarPos('w_min', 'image') * 100
    w_max = cv.getTrackbarPos('w_max', 'image') * 100
    h_min = cv.getTrackbarPos('h_min', 'image') * 10
    h_max = cv.getTrackbarPos('h_max', 'image') * 10

    ratio_min = cv.getTrackbarPos('ratio_min', 'image') * 0.1
    ratio_max = cv.getTrackbarPos('ratio_max', 'image') * 0.1

    extent_min = cv.getTrackbarPos('extent_min', 'image') * 0.01
    solid_min = cv.getTrackbarPos('solid_min', 'image') * 0.01

    # convert to HSV, create white color mask
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    low = np.array([hue_l, sat_l, val_l])
    high = np.array([hue_h, sat_h, val_h])
    mask = cv.inRange(img_hsv, low, high)

    # find contours in mask
    contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    contours_filtered = []
    for con in contours:

        # filter by area
        area = cv.contourArea(con)
        if area_min < area < area_max:

            # obtain rotated rectangle and filter by its width, height
            rect = cv.minAreaRect(con)
            (_, (w_a, h_a), angle) = rect
            if angle < 45:
                w, h = w_a, h_a
            else:
                w, h = h_a, w_a

            if w_min < w < w_max and h_min < h < h_max:

                # calculate and filter by ratio, extent and solidity
                ratio = w / h
                rect_area = w * h
                extent = area / rect_area
                con_hull = cv.convexHull(con)
                hull_area = cv.contourArea(con_hull)
                solidity = area / hull_area
                if ratio_min < ratio < ratio_max and extent_min < extent and solid_min < solidity:
                    contours_filtered.append(con_hull)

    # draw filtered contours and number of errors in train set
    cv.drawContours(img, contours_filtered, -1, (0, 0, 255), 10)
    err[cnt % cnt_max] = abs(len(contours_filtered) - 1)
    print(sum(err))

    # plot image
    img_res = cv.resize(img, None, fx=0.25, fy=0.25)
    cv.imshow('image', img_res)
