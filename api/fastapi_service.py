from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
import cv2
from PIL import Image
import io
import tempfile

app = FastAPI()

@app.post("/convert")
async def convert_video_to_bw_frame(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=True) as temp_file:
        temp_file.write(await file.read())
        temp_file.seek(0)  # Go back to the start of the file

        cap = cv2.VideoCapture(temp_file.name)
        success, frame = cap.read()  # Read the first frame
        if success:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
            is_success, buffer = cv2.imencode(".jpg", gray_frame)
            if is_success:
                # Convert buffer to a bytes-like object
                buffer_bytes = io.BytesIO(buffer)
                buffer_bytes.seek(0)  # Go to the start of the BytesIO object

                return StreamingResponse(buffer_bytes, media_type="image/jpeg")

    # If the process fails, return an error response
    return {"error": "Failed to process the video"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
