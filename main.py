from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from deepface import DeepFace
import cv2
import numpy as np
import base64
import re

from spotify import get_tracks_by_genre, emotion_to_genre  

app = FastAPI()

app.mount("/public", StaticFiles(directory="public"), name="public")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ImageData(BaseModel):
    image: str

def decode_base64_image(base64_str: str):
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    img_bytes = base64.b64decode(base64_data)
    np_arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img

@app.get("/")
def home():
    return FileResponse("public/index.html")

@app.post("/detect-emotion")
async def detect_emotion(data: ImageData):
    try:
        img = decode_base64_image(data.image)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        analysis = DeepFace.analyze(rgb_img, actions=['emotion'], enforce_detection=False)

        if isinstance(analysis, list) and len(analysis) > 0:
            top_emotion = analysis[0].get("dominant_emotion", "neutral").lower()
        else:
            top_emotion = "neutral"

        genre = emotion_to_genre.get(top_emotion, "chill")
        tracks = get_tracks_by_genre(genre)

        return {
            "emotion": top_emotion,
            "genre": genre,
            "tracks": tracks
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
