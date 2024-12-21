import cv2  # Ensure you're using opencv-python-headless
import torch
import numpy as np

def detect_traffic_jam(video_path, output_path, vehicle_threshold=10):
    # Load the YOLOv5 model
    model_path = './yolov5/runs/train/exp6/weights/best.pt'
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)

    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        detections = results.xyxy[0].numpy()

        vehicle_count = len(detections)
        if vehicle_count > vehicle_threshold:
            cv2.putText(frame, "Traffic Jam Detected!", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

        out.write(frame)

    cap.release()
    out.release()
