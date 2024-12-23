Traffic Jam and Accident-Prone Vehicle Detection

The Traffic Jam and Accident-Prone Vehicle Detection is a tool designed to analyze traffic jams and detect accident-prone vehicles from video footage using deep learning techniques. This document provides an overview of the project, step-by-step instructions for running the project, and hardware and software requirements.


Table of Contents

1. Project Overview
2. Features
3. System Requirements
4. Installation and Usage
5. Project Workflow


Project Overview

This project processes video footage to identify two key aspects of traffic analysis:

1. Traffic Jam Detection: Detects areas of congestion in the video.
2. Accident-Prone Vehicle Detection: Identifies vehicles that exhibit erratic or potentially dangerous behavior.


Features

- Upload video files in `.mp4` or `.avi` format.
- Real-time processing of traffic footage.
- Download processed video results with overlays.
- User-friendly interface built with **Streamlit**.


System Requirements

 Hardware Requirements

- Processor: Intel Core i5 or higher
- RAM: 8 GB or more
- GPU: NVIDIA GPU with CUDA support (optional for faster processing)
- Storage: At least 10 GB of free disk space

 Software Requirements

- Operating System: Windows 10/11, Linux, or macOS
- Python: Version 3.11.9
- OpenCV: Version 4.10.0
- Streamlit: Version 1.25.0
- TensorFlow: Version 2.13.0
- NumPy: Version 1.25.0


Installation and Usage

Follow these steps to set up the project:

1. Open the file is vscode
   

2. Install Dependencies:

   pip install -r requirements.txt
   

3. Run the Streamlit Application:

   streamlit run traffic_monitoring_dashboard.py


4. Upload Video:

   - Click on the "Upload a Video" section.
   - Choose a `.mp4` or `.avi` video file from your system.

5. Process Video:

   - Click on **Detect Traffic Jam** to analyze congestion.
   - Click on **Detect Accident-Prone Vehicles** to identify dangerous vehicles.

6. Download Results:

   - Once processing is complete, click on the download button to save the processed video.


Project Workflow

1. Data Input:

   - User uploads a video file.

2. Traffic Jam Detection:

   - The uploaded video is processed to identify regions of congestion using the `detect_traffic_jam` function.

3. Accident-Prone Vehicle Detection:

   - The video is analyzed to detect erratic vehicle behavior using the `detect_accident_prone_vehicles` function.

4. Output Generation:

   - Processed videos are saved and made available for download.

5. User Interface:

   - Results are displayed in a visually appealing Streamlit dashboard.

 Detailed Workflow:

  Phase 1: Data Input and Preprocessing
- The user uploads the video via the dashboard.
- The video is validated for supported formats (.mp4 or .avi).

  Phase 2: Traffic Jam Detection
- The video frames are extracted using OpenCV.
- Object detection algorithms analyze vehicle density in each frame.
- Areas with high vehicle density are marked as traffic jams.

  Phase 3: Accident-Prone Vehicle Detection
- The system tracks vehicle movements frame-by-frame.
- Speed and trajectory of each vehicle are calculated.
- Erratic or sudden movements are flagged as potential accident-prone behavior.

  Phase 4: Output Generation
- Overlay annotations are added to highlight traffic jams and accident-prone vehicles.
- The processed video is saved in .mp4 format.

  Phase 5: User Interaction
- The processed video can be downloaded via the dashboard.

