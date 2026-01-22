# import cv2

# cap= cv2.VideoCapture('Test.mp4')
# success,frame=cap.read()

# if success:
#     h,w,c=frame.shape


# print("Video Resolution:", w, "x", h)
# print("Channels:", c)

# cap.release()





# british_highway
# Video Resolution: 1364 x 768
# Channels: 3

# road_traffic
# Video Resolution: 640 x 360
# Channels: 3



# import sys
# print("PYTHON:", sys.executable)

# print('hello')


import cv2

cap = cv2.VideoCapture("Test.mp4")

points = []

def mousePoints(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)
        points.append((x, y))

        if len(points) == 2:
            print("Line coordinates:", points)

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", mousePoints)

while True:
    success, img = cap.read()
    if not success:
        break

    # Draw clicked points
    for point in points:
        cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED)

    if len(points) == 2:
        cv2.line(img, points[0], points[1], (0, 0, 255), 3)

    cv2.imshow("Frame", img)
    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = int(1000 / fps)

    if cv2.waitKey(delay) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
