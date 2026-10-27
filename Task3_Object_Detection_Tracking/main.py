
from ultralytics import YOLO
import cv2

# Load the pretrained YOLO model
model = YOLO("yolo11n.pt")

# Open the input video
video_path = "input.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open input.mp4")
    print("Make sure input.mp4 is in the same folder as main.py.")
    raise SystemExit

# Get video information
fps = cap.get(cv2.CAP_PROP_FPS)
original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(f"Video size: {original_width} x {original_height}")
print(f"Video FPS: {fps:.2f}")
print("Object detection and tracking started.")
print("Press Q to quit.")

# Set the maximum display size
max_width = 960
max_height = 600

window_name = "CodeAlpha - Object Detection and Tracking"

cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, max_width, max_height)

while True:
    success, frame = cap.read()

    if not success:
        break

    # Detect objects and maintain tracking IDs across frames
    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        conf=0.35,
        verbose=False
    )

    # Draw bounding boxes, labels, and tracking IDs
    annotated_frame = results[0].plot()

    # Resize without changing the aspect ratio
    height, width = annotated_frame.shape[:2]

    scale = min(
        max_width / width,
        max_height / height,
        1.0
    )

    if scale < 1.0:
        display_width = int(width * scale)
        display_height = int(height * scale)

        display_frame = cv2.resize(
            annotated_frame,
            (display_width, display_height),
            interpolation=cv2.INTER_AREA
        )
    else:
        display_frame = annotated_frame

    # Display the annotated video
    cv2.imshow(window_name, display_frame)

    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

print("Object detection and tracking finished.")
