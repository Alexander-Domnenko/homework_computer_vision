import numpy as np
import cv2


def draw_contour(frame, mask, contour_color):
    contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(c)
        if radius > 30:
            cv2.circle(frame, (int(x), int(y)), int(radius), contour_color, 3)
            position = (int(x),int(y))
            return position

lower_yellow = np.array([18, 80, 100])
upper_yellow = np.array([26, 230, 255])

lower_green = np.array([50, 50, 50])
upper_green = np.array([70, 255, 255])

lower_blue = np.array([92, 150, 120])
upper_blue = np.array([105, 255, 255])

lower_orange = np.array([5, 100, 200])
upper_orange =np.array([10, 200, 255])

cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)
cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.GaussianBlur(frame,(11,11), 0)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask_yellow = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
    mask_yellow = cv2.dilate(mask_yellow, None, iterations=2)

    mask_green = cv2.inRange(hsv_frame, lower_green, upper_green)
    mask_green = cv2.dilate(mask_green, None, iterations=2)

    mask_blue = cv2.inRange(hsv_frame, lower_blue, upper_blue)
    mask_blue = cv2.dilate(mask_blue, None, iterations=2)

    mask_orange = cv2.inRange(hsv_frame, lower_orange, upper_orange)
    mask_orange = cv2.dilate(mask_orange, None, iterations=2)

    center_green = draw_contour(frame, mask_green, (0, 255, 0))
    center_blue = draw_contour(frame, mask_blue, (255, 0, 0))
    center_yellow = draw_contour(frame, mask_yellow, (80, 255, 255))
    center_orange = draw_contour(frame, mask_orange, (0, 200, 255))

    
    
    # if center_blue != None and center_green != None and center_yellow != None and center_orange == None:
    #     if center_yellow[0] > center_blue[0] and center_blue[0] > center_green[0]:
    #         cv2.putText(frame, 'win 3 balls', (60,60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))   #[yellow,orange,
                                                                                               #  blue,green]
    if center_blue != None and center_green != None and center_yellow != None and center_orange != None:
        if center_yellow[0] < center_green[0] and center_yellow[1] < center_green[1] and center_orange[1] < center_blue[1] and center_blue[0] < center_orange[0] and center_yellow[0]<center_orange[0] and center_blue[0] < center_green[0]:
            cv2.putText(frame, 'win 4 balls', (60,60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
        
    cv2.imshow("Camera", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()