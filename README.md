# Video Cutter
A web application (built with [Trae](https://www.trae.ai/download)) that allows users to upload videos and cut them to specific time segments using a simple and intuitive interface.

## Features

- Upload video files via drag-and-drop or file selection
- Interactive timeline slider to select start and end points
- Lossless video cutting using FFmpeg
- Instant preview of the video
- Download cut videos

## Technologies Used

- Backend: FastAPI (Python)
- Frontend: HTML, CSS, JavaScript
- Video Processing: FFmpeg (via ffmpeg-python)
- UI Components: Bootstrap, noUiSlider

## Installation

1. Clone the repository

2. Install the required dependencies:

```bash
conda create -n video_cutter python=3.10.13 -y

conda activate video_cutter

pip install -r requirements.txt
```

3. Make sure FFmpeg is installed on your system. If not, install it:
   - Windows: Download from [FFmpeg website](https://ffmpeg.org/download.html) or install via Chocolatey
   - macOS: `brew install ffmpeg`
   - Linux: `apt-get install ffmpeg` or equivalent for your distribution

## Usage

1. Start the application:

```bash
python main.py
```

Or use uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. Open your browser and navigate to `http://localhost:8000`

3. Upload a video file by dragging and dropping or clicking the upload button

4. Use the slider to select the start and end points of the segment you want to cut

5. Click the "Cut Video" button to process the video

6. Once processing is complete, click the "Download" button to save the cut video

## Project Structure

```
├── Dockerfile        # Docker configuration
├── main.py           # FastAPI application
├── requirements.txt  # Python dependencies
├── static/           # Static files
├── templates/        # HTML templates
│   └── index.html    # Main application page
├── uploads/          # Temporary storage for uploaded videos
└── processed/        # Storage for processed videos
```

## Docker Deployment

1. Build the Docker image:

```bash
docker build -t video-cutter .
```

2. Run the container:

```bash
docker run -d -p 8000:8000 --name video-cutter-app video-cutter
```
Or run the pre-built Docker image: `samge/video-cutter`

```bash
docker run -itd --restart=always -p 8000:8000 --name video-cutter-app samge/video-cutter
```

3. Access the application at `http://localhost:8000`

To stop the container:

```bash
docker stop video-cutter-app
```

To remove the container:

```bash
docker rm video-cutter-app
```

## Notes

- The application uses FFmpeg's copy mode for lossless cutting, which is fast but requires cutting at keyframes for precise results
- Uploaded and processed videos are stored on the server and not automatically cleaned up

## License

MIT

## ScreenShot
![image](https://github.com/user-attachments/assets/344e266f-82a8-4b2b-9e61-7cfec700e3f8)

![image](https://github.com/user-attachments/assets/30d1eb81-e3da-4601-b0cd-9f57bcd5d1de)

