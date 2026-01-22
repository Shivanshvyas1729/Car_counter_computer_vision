preparing deep sort with YOLO


🧠 VEHICLE COUNTING PROJECT – PSEUDOCODE (STEP-BY-STEP)
STEP-0️⃣ Setup
Load YOLO model
Open video
Load mask image
Define counting line (2 points)
Define line width (tolerance)
Initialize SORT tracker
Create empty list for counted IDs

STEP-1️⃣ Pre-calculation (ONE TIME)
Extract line points (x1, y1, x2, y2)

Compute:
    dx = x2 - x1
    dy = y2 - y1
    line_length = sqrt(dx^2 + dy^2)


👉 Ye sirf diagonal line ke liye math setup hai

STEP-2️⃣ Start video loop
WHILE video has frames:
    Read frame
    IF frame not available:
        break loop

STEP-3️⃣ Preprocess frame
Apply mask on frame
Pass masked frame to YOLO
Create empty detections list

STEP-4️⃣ Object Detection
FOR each detection result:
    FOR each detected box:
        Extract bounding box (x1, y1, x2, y2)
        Get confidence
        Get class label

        IF object is vehicle AND confidence is high:
            Add [x1, y1, x2, y2, confidence] to detections

STEP-5️⃣ Tracking (SORT)
Pass detections to SORT tracker
Receive tracked objects with IDs

STEP-6️⃣ Draw counting line (visual only)
Draw red line using (x1, y1) → (x2, y2)


⚠️ Ye sirf display ke liye hai
Counting logic alag hota hai

STEP-7️⃣ For each tracked object
FOR each tracked object:
    Extract bounding box and ID
    Compute center point (cx, cy)
    Draw bounding box
    Draw ID
    Draw center dot

STEP-8️⃣ CORE LOGIC – LINE CROSS CHECK (IMPORTANT)
Compute distance of (cx, cy) from line using point-to-line formula

IF distance < LINE_WIDTH:
    IF ID not already counted:
        Add ID to counted list
        Draw green line (count happened)


👉 Yahi actual counting logic hai
👉 Ye horizontal, vertical, diagonal — sab pe kaam karta hai

STEP-9️⃣ Display total count
Show "Count = number of unique IDs counted"
Show frame

STEP-🔟 Exit condition
IF ESC key pressed:
    break loop

STEP-1️⃣1️⃣ Cleanup
Release video
Close all windows