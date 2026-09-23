import cv2
filename = "apple.png"

img = cv2.imread(filename)

img = cv2.resize(img, (500, 500))

# display regular image
cv2.imshow("Result", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# tune these ranges to match your apple's actual colors
red_mask = cv2.inRange(hsv, (0, 100, 100), (10, 255, 255))
white_mask = cv2.inRange(hsv, (0, 0, 200), (180, 30, 255))
green_mask = cv2.inRange(hsv, (30, 40, 40), (90, 255, 255))
brown_mask = cv2.inRange(hsv, (10, 50, 20), (30, 255, 255))

red_img = cv2.bitwise_and(img, img, mask=red_mask)
white_img = cv2.bitwise_and(img, img, mask=white_mask)
green_img = cv2.bitwise_and(img, img, mask=green_mask)
brown_img = cv2.bitwise_and(img, img, mask=brown_mask)

cv2.imshow("Result", red_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imshow("Result", white_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imshow("Result", green_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imshow("Result", brown_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

"""
blue_img = img.copy()
green_img = img.copy()
red_img = img.copy()

# [rows, col, color_channels], 0 = blue, 1 = green, 2 = red
blue_img[:,:,1] = 0
blue_img[:,:,2] = 0

green_img[:,:,0] = 0
green_img[:,:,2] = 0

red_img[:,:,0] = 0
red_img[:,:,1] = 0

cv2.imshow("Result", blue_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imshow("Result", green_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imshow("Result", red_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""