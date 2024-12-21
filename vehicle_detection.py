import torch
import cv2
import numpy as np

def detect_traffic_jam(video_path, output_path, vehicle_threshold=10):
    """
    Detect traffic jam in a video based on the number of vehicles in each frame.

    Args:
        video_path (str): Path to the input video.
        output_path (str): Path to save the output annotated video.
        vehicle_threshold (int): Number of vehicles required to detect a traffic jam.
    """
    # Load the YOLOv5 model
    model_path = './yolov5/runs/train/exp6/weights/best.pt'
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Perform inference
        results = model(frame)
        detections = results.xyxy[0].numpy()

        # Count the number of vehicles detected in the frame
        vehicle_count = len(detections)

        # If the number of detected vehicles exceeds the threshold, mark as traffic jam
        if vehicle_count > vehicle_threshold:
            cv2.putText(frame, "Traffic Jam Detected!", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

        
        

        # Write the frame with detections to the output video
        out.write(frame)

        # Optional: Uncomment the next line to show the frame with detections during debugging
        # cv2.imshow('Frame', frame)

        # Exit the loop if 'q' is pressed (if displaying the window)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    # Release everything when done
    cap.release()
    out.release()
    # cv2.destroyAllWindows()  # Not needed for Streamlit
