from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import mediapipe as mp

app = FastAPI(title="EyeViaController API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "EyeViaController API"}

@app.post("/landmarks")
async def get_landmarks(image: UploadFile = File(...)):
    data = await image.read()
    np_arr = np.frombuffer(data, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if frame is None:
        raise HTTPException(status_code=400, detail="Invalid image file")

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb_frame)
    if not result.multi_face_landmarks:
        return {"faces": 0, "landmarks": []}

    face = result.multi_face_landmarks[0]
    all_landmarks = []
    for i, lm in enumerate(face.landmark):
        all_landmarks.append({"id": i, "x": lm.x, "y": lm.y, "z": lm.z})
    return {
        "faces": len(result.multi_face_landmarks),
        "landmarks": all_landmarks,
    }
