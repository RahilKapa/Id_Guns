import os
import subprocess
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from werkzeug.utils import secure_filename
import regex as re

import torch

apple = "CPU is available"

# Check if CUDA is available
if torch.cuda.is_available():
    device = torch.device("cuda")
    apple = "GPU is available"
else:
    device = torch.device("cpu")
    


app = FastAPI()

origins = [
    "https://vercel-front-end-git-main-rahilkapa.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOADS_DIR = "uploads"


@app.post("/results")
async def results(file: UploadFile = File(...)):
    # Extract the filename from the UploadFile object

    filename = secure_filename(file.filename)

    # Prepare the path to save the uploaded image
    save_path = os.path.join(UPLOADS_DIR, filename)

    # Save the uploaded image to the specified path
    with open(save_path, "wb") as buffer:
        buffer.write(await file.read())

    # Prepare the command to call the inference script
    print(save_path)
    cmd = f'python3 recognize-anything/inference_ram.py --image {save_path} --pretrained recognize-anything/pretrained/ram_swin_large_14m.pth'

    # Call the model for inference
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    predicted_object = result.stdout.strip()

    index = predicted_object.find("Image Tags:")
    print(predicted_object)
    print("hello")
    
    if index != -1:
        predicted_object = predicted_object[index+len("Image Tags:"):].strip()
        # Remove Mandarin characters using Unicode range
        predicted_object = re.sub(r'[\u4e00-\u9fff|:/]+', '', predicted_object)

    


    return {"predicted_object": predicted_object + apple}

