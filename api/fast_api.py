from fastapi import FastAPI, UploadFile
from fastapi.param_functions import File
from fastapi.responses import JSONResponse
import subprocess
import os



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
async def save_file(
    video_file: UploadFile = File(...)):

    # check if the file is a video
    if video_file.content_type != "video/mp4":
        return JSONResponse(
            status_code=400, content={"message": "Only video files are allowed"}
        )

    video_name = f"{uuid.uuid4()}.mp4"
    #save the file in video input directory
    save_directory = "../VideoInput"
    video_path = os.path.join(save_directory, video_name)


    with open(video_path, "wb") as buffer:
        contents = await video_file.read()
        buffer.write(contents)
