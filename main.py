# cspell:disable

# YOLO model import (object detection ke liye)
from ultralytics import YOLO

# OpenCV import (video + drawing ke liye)
import cv2

from sort import Sort
import numpy as np

# Pretrained YOLOv8 nano model load
# 'yolov8n.pt' fast & lightweight model hai
model = YOLO("yolov8n.pt")

# Video open
cap = cv2.VideoCapture("Test.mp4")

mask = cv2.imread("mask1.png")

# ================= COUNTING LINE =================
# Line coordinates (mouse se nikaale hue)
count_line = [269, 612, 720, 604]

# Line width (REAL counting width, perpendicular direction)
LINE_WIDTH = 20

# Line points
x1l, y1l, x2l, y2l = count_line

# Line direction
dx = x2l - x1l
dy = y2l - y1l

# Line length
line_len = np.hypot(dx, dy)

# SORT tracker
tracker = Sort(max_age=50, min_hits=4, iou_threshold=0.3)

# Total counted IDs
totalCount = []

# Window ko resizable banane ke liye
cv2.namedWindow("Webcam YOLO", cv2.WINDOW_NORMAL)

# ================= MAIN LOOP =================
while True:

    success, img = cap.read()
    if not success:
        break

    # Mask apply
    imgRegion = cv2.bitwise_and(img, mask)

    # YOLO detection
    results = model(imgRegion, stream=True, verbose=False)

    detections = np.empty((0, 5))

    # ================= DETECTION LOOP =================
    for r in results:
        for box in r.boxes:

            coords = box.xyxy[0]
            x1, y1, x2, y2 = map(int, coords)

            conf = float(box.conf[0])
            cls = int(box.cls[0])
            label = model.names[cls]

            # Sirf vehicles
            if label in ["car", "truck", "bus", "motorbike"] and conf > 0.35:
                current = np.array([x1, y1, x2, y2, conf])
                detections = np.vstack((detections, current))

    # ================= TRACKING =================
    resultTracker = tracker.update(detections)

    # Draw counting line (RED – normal)
    cv2.line(
        img,
        (x1l, y1l),
        (x2l, y2l),
        (0, 0, 255),
        10
    )

    # ================= TRACK LOOP =================
    for x1, y1, x2, y2, _id in resultTracker:
        x1, y1, x2, y2, _id = map(int, (x1, y1, x2, y2, _id))

        # Center point
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)

        # Bounding box
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 2)

        # ID text
        cv2.putText(
            img,
            f"ID: {_id}",
            (x1, y1 - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 0, 255),
            2
        )

        # Center dot
        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        # ================= REAL LINE CROSSING CHECK =================
        # Point to line distance (diagonal safe)
        distance = abs(
            dy * cx - dx * cy + x2l * y1l - y2l * x1l
        ) / line_len

        if distance < LINE_WIDTH:
            if _id not in totalCount:
                totalCount.append(_id)

                # Count hone par GREEN line
                cv2.line(
                    img,
                    (x1l, y1l),
                    (x2l, y2l),
                    (0, 255, 0),
                    10
                )

    # ================= DISPLAY COUNT =================
    cv2.putText(
        img,
        f"Count: {len(totalCount)}",
        (50, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.5,
        (0, 255, 255),
        4
    )

    cv2.imshow("Webcam YOLO", img)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
