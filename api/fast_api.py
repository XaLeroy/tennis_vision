from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
import cv2
from PIL import Image
import io
import tempfile
import os
import uuid

app = FastAPI()

@app.get("/")
def root():
    return {
    'greeting': 'Welcome to tennis vision API!'
}

@app.get("/predict")
def predict(minimap=0, bounce=0, input_video_name=None, ouput_video_name=None):
    subprocess.run(["python3", "predict_video.py", f"--input_video_path=VideoInput/{input_video_name}.mp4", f"--output_video_path=VideoOutput/{ouput_video_name}.mp4", f"--minimap={minimap}", f"--bounce={bounce}"])
    return {'greeting': "Please find below your treated videos"}


@app.post("/savefile")
async def convert_video_to_bw_frame(file: UploadFile = File(...)):

    #save the file in video input directory
    video_name = f"{uuid.uuid4()}.mp4"
    save_directory = "/home/rs_munozcarrasco/tennis_vision/api/apivideos/"
    video_path = os.path.join(save_directory, video_name)
    with open(video_path, "wb") as buffer:
        contents = await file.read()
        buffer.write(contents)


    #with tempfile.NamedTemporaryFile(delete=True) as temp_file:
    with open(video_path, "rb") as temp_file:
        #temp_file.write(await file.read())
        #temp_file.seek(0)  # Go back to the start of the file

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

