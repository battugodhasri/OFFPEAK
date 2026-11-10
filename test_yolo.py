
import cv2
from ultralytics import YOLO

# 1. Load YOLO model
print("Loading YOLO model...")
model = YOLO("yolo11s.pt")

# 2. Open resized crowd video
video_path = "videos/crowd.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("ERROR: Cannot open video")
    exit()

print("Video opened successfully!")
print("Starting person detection...")

frame_number = 0

# 3. Create smaller video display window
window_name = "OFFPEAK - Person Detection"

cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, 900, 550)

# 4. Process video frame by frame
while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame_number += 1

    # 5. Detect only people (class ID 0)
    results = model.predict(
    source=frame,
    classes=[0],
    conf=0.10,
    imgsz=1000,
    max_det=1500,
    device="cpu",
    verbose=False
)

    result = results[0]

    # 6. Count detected people
    person_count = len(result.boxes)

    # 7. Draw bounding boxes
    output = result.plot(
        line_width=2,
        labels=True,
        conf=True
    )

    # 8. Display people count
    cv2.putText(
        output,
        f"People Detected: {person_count}",
        (20, 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # 9. Save first processed frame
    if frame_number == 1:
        cv2.imwrite("yolo_debug.jpg", output)
        print("First frame detections:", person_count)
        print("Saved yolo_debug.jpg")

    # 10. Display video
    cv2.imshow(window_name, output)

    # Press Q to stop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 11. Release resources
cap.release()
cv2.destroyAllWindows()

print("Detection completed!")
