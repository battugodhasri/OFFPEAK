import cv2
import numpy as np
import csv
from ultralytics import YOLO

# ------------------------------------------------
# MODEL
# ------------------------------------------------

model = YOLO("yolo11n.pt")

# ------------------------------------------------
# VIDEO
# ------------------------------------------------

video = cv2.VideoCapture("videos/crowd.mp4")

if not video.isOpened():
    print("Could not open crowd.mp4")
    exit()

# ------------------------------------------------
# VIDEO SIZE
# ------------------------------------------------

width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

print("Video size:", width, "x", height)

# ------------------------------------------------
# DISPLAY
# ------------------------------------------------

display_width = 800
display_height = 450

window_name = "OFFPEAK - Multi Zone Counting"

cv2.namedWindow(
    window_name,
    cv2.WINDOW_NORMAL
)

cv2.resizeWindow(
    window_name,
    display_width,
    display_height
)

# ------------------------------------------------
# ZONES
# ------------------------------------------------

zones = {
    "Zone 1": [],
    "Zone 2": [],
    "Zone 3": []
}

current_zone = "Zone 1"
selecting = True

# ------------------------------------------------
# HISTORICAL CSV
# ------------------------------------------------

csv_file = open(
    "crowd_data.csv",
    "w",
    newline=""
)

csv_writer = csv.writer(csv_file)

csv_writer.writerow([
    "video_time_seconds",
    "zone1",
    "zone2",
    "zone3",
    "total"
])

csv_file.flush()

last_log_time = -5

# ------------------------------------------------
# LIVE CSV
# ------------------------------------------------

live_file = open(
    "live_data.csv",
    "w",
    newline=""
)

live_writer = csv.writer(live_file)

live_writer.writerow([
    "video_time_seconds",
    "zone1",
    "zone2",
    "zone3",
    "total"
])

live_file.flush()

# ------------------------------------------------
# MOUSE CALLBACK
# ------------------------------------------------

def mouse_callback(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:

        original_x = int(
            x * width / display_width
        )

        original_y = int(
            y * height / display_height
        )

        zones[current_zone].append(
            (original_x, original_y)
        )

        print(
            current_zone,
            "Point added:",
            original_x,
            original_y
        )


cv2.setMouseCallback(
    window_name,
    mouse_callback
)

# ------------------------------------------------
# FIRST FRAME
# ------------------------------------------------

ret, first_frame = video.read()

if not ret:

    print("Could not read video")

    video.release()
    csv_file.close()
    live_file.close()

    exit()

# ------------------------------------------------
# ZONE SELECTION
# ------------------------------------------------

while selecting:

    zone_frame = first_frame.copy()

    for zone_name, points in zones.items():

        if len(points) == 0:
            continue

        if zone_name == "Zone 1":
            color = (0, 255, 0)

        elif zone_name == "Zone 2":
            color = (255, 0, 0)

        else:
            color = (0, 0, 255)

        # Points
        for point in points:

            cv2.circle(
                zone_frame,
                point,
                7,
                color,
                -1
            )

        # Lines
        if len(points) > 1:

            for i in range(
                len(points) - 1
            ):

                cv2.line(
                    zone_frame,
                    points[i],
                    points[i + 1],
                    color,
                    3
                )

        # Close polygon
        if len(points) >= 3:

            cv2.line(
                zone_frame,
                points[-1],
                points[0],
                color,
                3
            )

    # ------------------------------------------------
    # INSTRUCTIONS
    # ------------------------------------------------

    cv2.putText(
        zone_frame,
        f"Drawing: {current_zone}",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.putText(
        zone_frame,
        "Click points | 2=Zone2 | 3=Zone3 | "
        "S=Start | R=Reset | Q=Quit",
        (20, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )

    display_frame = cv2.resize(
        zone_frame,
        (
            display_width,
            display_height
        )
    )

    cv2.imshow(
        window_name,
        display_frame
    )

    key = cv2.waitKey(1) & 0xFF

    # Zone 2
    if key == ord("2"):

        current_zone = "Zone 2"

        print("Now drawing Zone 2")

    # Zone 3
    elif key == ord("3"):

        current_zone = "Zone 3"

        print("Now drawing Zone 3")

    # Reset
    elif key == ord("r"):

        zones[current_zone].clear()

        print(
            current_zone,
            "reset"
        )

    # Start
    elif key == ord("s"):

        valid = True

        for zone_name, points in zones.items():

            if len(points) < 3:

                print(
                    zone_name,
                    "needs at least 3 points."
                )

                valid = False

        if valid:

            selecting = False

            print("All zones saved!")

    # Quit
    elif key == ord("q"):

        video.release()
        csv_file.close()
        live_file.close()

        cv2.destroyAllWindows()

        exit()

# ------------------------------------------------
# RESTART VIDEO
# ------------------------------------------------

video.set(
    cv2.CAP_PROP_POS_FRAMES,
    0
)

print("\nStarting crowd detection...")
print("Live data will be written to live_data.csv\n")

# ------------------------------------------------
# VIDEO LOOP
# ------------------------------------------------

while True:

    ret, frame = video.read()

    if not ret:

        print("\nVideo finished.")

        break

    # ------------------------------------------------
    # YOLO TRACKING
    # ------------------------------------------------

    results = model.track(
        source=frame,
        persist=True,
        classes=[0],
        conf=0.15,
        imgsz=1536,
        max_det=500,
        tracker="bytetrack.yaml"
    )

    annotated_frame = results[0].plot()

    # ------------------------------------------------
    # COUNTS
    # ------------------------------------------------

    zone_counts = {
        "Zone 1": 0,
        "Zone 2": 0,
        "Zone 3": 0
    }

    total_people = 0

    # ------------------------------------------------
    # TRACKED PEOPLE
    # ------------------------------------------------

    if results[0].boxes.id is not None:

        boxes = (
            results[0]
            .boxes
            .xyxy
            .cpu()
            .numpy()
        )

        total_people = len(boxes)

        for box in boxes:

            x1, y1, x2, y2 = box

            center_x = int(
                (x1 + x2) / 2
            )

            center_y = int(y2)

            for zone_name, points in zones.items():

                inside = cv2.pointPolygonTest(
                    np.array(points),
                    (
                        center_x,
                        center_y
                    ),
                    False
                )

                if inside >= 0:

                    zone_counts[
                        zone_name
                    ] += 1

    # ------------------------------------------------
    # VIDEO TIME
    # ------------------------------------------------

    current_video_time = (
        video.get(
            cv2.CAP_PROP_POS_MSEC
        ) / 1000
    )

    # ------------------------------------------------
    # WRITE LIVE DATA
    # ------------------------------------------------

    live_writer.writerow([
        round(
            current_video_time,
            2
        ),
        zone_counts["Zone 1"],
        zone_counts["Zone 2"],
        zone_counts["Zone 3"],
        total_people
    ])

    # VERY IMPORTANT
    # Force data to disk immediately
    live_file.flush()

    # ------------------------------------------------
    # WRITE HISTORICAL DATA
    # ------------------------------------------------

    if (
        current_video_time
        - last_log_time
        >= 5
    ):

        csv_writer.writerow([
            round(
                current_video_time,
                2
            ),
            zone_counts["Zone 1"],
            zone_counts["Zone 2"],
            zone_counts["Zone 3"],
            total_people
        ])

        csv_file.flush()

        last_log_time = current_video_time

        print(
            f"Saved: "
            f"{round(current_video_time, 2)}s | "
            f"Z1={zone_counts['Zone 1']} | "
            f"Z2={zone_counts['Zone 2']} | "
            f"Z3={zone_counts['Zone 3']} | "
            f"Total={total_people}"
        )

    # ------------------------------------------------
    # DRAW ZONES
    # ------------------------------------------------

    for zone_name, points in zones.items():

        if zone_name == "Zone 1":

            color = (0, 255, 0)

        elif zone_name == "Zone 2":

            color = (255, 0, 0)

        else:

            color = (0, 0, 255)

        cv2.polylines(
            annotated_frame,
            [np.array(points)],
            True,
            color,
            4
        )

    # ------------------------------------------------
    # DISPLAY COUNTS
    # ------------------------------------------------

    cv2.putText(
        annotated_frame,
        f"ZONE 1: {zone_counts['Zone 1']}",
        (30, 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 0),
        3
    )

    cv2.putText(
        annotated_frame,
        f"ZONE 2: {zone_counts['Zone 2']}",
        (30, 85),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (255, 0, 0),
        3
    )

    cv2.putText(
        annotated_frame,
        f"ZONE 3: {zone_counts['Zone 3']}",
        (30, 125),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 0, 255),
        3
    )

    cv2.putText(
        annotated_frame,
        f"TOTAL: {total_people}",
        (30, 165),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (255, 255, 255),
        3
    )

    # ------------------------------------------------
    # DISPLAY
    # ------------------------------------------------

    display_frame = cv2.resize(
        annotated_frame,
        (
            display_width,
            display_height
        )
    )

    cv2.imshow(
        window_name,
        display_frame
    )

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):

        break

# ------------------------------------------------
# CLEANUP
# ------------------------------------------------

video.release()

csv_file.close()

live_file.close()

cv2.destroyAllWindows()

print("\nOFFPEAK processing stopped.")