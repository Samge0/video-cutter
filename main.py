from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import ffmpeg
import os
from pathlib import Path

app = FastAPI()

# Create directories for uploads and processed videos
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
PROCESSED_DIR = BASE_DIR / "processed"

for dir_path in [UPLOAD_DIR, PROCESSED_DIR]:
    dir_path.mkdir(exist_ok=True)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    return {"filename": file.filename}

@app.post("/cut-video")
async def cut_video(request: Request):
    data = await request.json()
    filename = data["filename"]
    start_time = data["start_time"]
    end_time = data["end_time"]
    duration = end_time - start_time
    input_path = UPLOAD_DIR / filename
    output_filename = f"cut_{filename}"
    output_path = PROCESSED_DIR / output_filename
    
    try:
        # Get keyframe before the start time
        probe = ffmpeg.probe(str(input_path))
        video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
        frame_rate = eval(video_info['r_frame_rate'])
        
        # Perform lossless cut using ffmpeg with proper stream alignment
        # Using both ss in input and output to ensure accurate cutting
        stream = ffmpeg.input(str(input_path))
        stream = ffmpeg.output(
            stream,
            str(output_path),
            ss=start_time,
            to=end_time,  # Use 'to' instead of 't' for more precise end time
            c='copy',  # Use copy mode for lossless cutting
            force_key_frames='expr:gte(t,n_forced*1)',
            max_muxing_queue_size=9999,
            avoid_negative_ts='make_zero',  # Ensure proper timestamp alignment
            acodec='copy',
            vcodec='copy',
            vsync='passthrough',
            movflags='faststart'  # Enable streaming optimization
        )
        ffmpeg.run(stream, overwrite_output=True)
        
        return {"success": True, "output_filename": output_filename}
    except ffmpeg.Error as e:
        return {"success": False, "error": str(e)}

@app.get("/download/{filename}")
async def download_video(filename: str):
    file_path = PROCESSED_DIR / filename
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="video/mp4"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)