import torch
import cv2
import numpy as np

def detect_accident_prone_vehicles(video_path, output_path):
    # Load YOLOv5 model
    model_path = './yolov5/runs/train/exp6/weights/best.pt'
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)

    # Open video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Cannot open video.")
        return

    # Video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    # ROI and speed thresholds
    roi_top, roi_bottom = int(height * 0.6), int(height * 0.7)
    speed_threshold_high = 100
    speed_threshold_low = 20

    # Vehicle tracking
    vehicle_positions = {}

    # Define a fixed pixel-to-meter conversion factor
    pixel_to_meter_factor = 0.015  # Example: 1 pixel = 0.05 meters (adjust based on your setup)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Draw two horizontal lines for ROI
        cv2.line(frame, (0, roi_top), (width, roi_top), (255, 0, 0), 2)
        cv2.line(frame, (0, roi_bottom), (width, roi_bottom), (255, 0, 0), 2)

        # YOLOv5 inference
        results = model(frame)
        detections = results.pandas().xyxy[0]

        current_time = cap.get(cv2.CAP_PROP_POS_FRAMES) / fps  # Time in seconds

        for i, row in detections.iterrows():
            label = row['name']
            if label in ['car', 'truck', 'bus']:
                x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2

                # Check if vehicle is in ROI
                if roi_top <= center_y <= roi_bottom:
                    vehicle_id = f"{label}_{i}"

                    # Draw bounding box and label
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                    # Check previous position and time
                    if vehicle_id in vehicle_positions:
                        prev_center, prev_time = vehicle_positions[vehicle_id]
                        distance_pixels = np.linalg.norm(np.array([center_x, center_y]) - np.array(prev_center))

                        # Convert pixel distance to meters
                        distance_meters = distance_pixels * pixel_to_meter_factor
                        time_diff = current_time - prev_time

                        if time_diff > 0:
                            # Calculate speed (km/h)
                            speed_kmh = (distance_meters / time_diff) * 3600 / 1000

                            # Display speed
                            cv2.putText(frame, f"Speed: {speed_kmh:.2f} km/h",
                                        (x1, y1 - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

                            # Check speed thresholds
                            if speed_kmh > speed_threshold_high or speed_kmh < speed_threshold_low:
                                cv2.putText(frame, f"Accident-Prone!",
                                            (x1, y1 - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                                cv2.circle(frame, (center_x, center_y), 60, (0, 0, 255), 2)

                    # Update vehicle position
                    vehicle_positions[vehicle_id] = ([center_x, center_y], current_time)

        # Write frame
        out.write(frame)

    cap.release()
    out.release()
    print(f"Detection completed and saved to {output_path}.")
