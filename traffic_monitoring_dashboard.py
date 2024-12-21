import streamlit as st
import os
from vehicle_detection import detect_traffic_jam
from accident_area_prediction import detect_accident_prone_vehicles

# Set the page configuration
st.set_page_config(
    page_title="Traffic Analysis Dashboard",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# App header with a title and description
st.markdown(
    """
    <div style="background-color:#DED1BD;padding:10px;border-radius:5px;">
        <h2 style="color:BLACK;text-align:center;">🚦 Traffic Jam and Accident-Prone Vehicle Detection 🚦</h1>
        <p style="color:grey;text-align:center;">Analyze traffic jams and accident-prone vehicles from video footage.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Sidebar for navigation and instructions
st.sidebar.title("📂 Upload and Process")
st.sidebar.write("1. Upload a video file.\n2. Choose the type of detection.\n3. Download the processed video.")

# File uploader
uploaded_file = st.file_uploader("🎥 Upload a Video", type=["mp4", "avi"])

if uploaded_file is not None:
    # Save the uploaded video to a temporary file
    video_path = "uploaded_video.mp4"
    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())

    # Inform the user about the successful upload
    st.success("Video uploaded successfully!")
    
    # Initialize output path for the most recent processed video
    processed_video_path = None

    # Horizontal layout for detection options
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🚗 Detect Traffic Jam"):
            with st.spinner("Processing traffic jam detection..."):
                processed_video_path = "output_traffic_jam.mp4"
                detect_traffic_jam(video_path, processed_video_path)
            st.success("Traffic jam detection completed!")

    with col2:
        if st.button("🚨 Detect Accident-Prone Vehicles"):
            with st.spinner("Processing accident-prone vehicle detection..."):
                processed_video_path = "output_accident_area.mp4"
                detect_accident_prone_vehicles(video_path, processed_video_path)
            st.success("Accident-prone vehicle detection completed!")

    # Single download button for the most recent processed video
    if processed_video_path and os.path.exists(processed_video_path):
        with open(processed_video_path, "rb") as f:
            st.download_button(
                label="⬇️ Download Processed Video",
                data=f,
                file_name=os.path.basename(processed_video_path),
                mime="video/mp4",
            )

    # Clean up the temporary video file after processing
    if os.path.exists(video_path):
        os.remove(video_path)

else:
    # Display instructions when no file is uploaded
    st.info("Please upload a video to start processing.")
