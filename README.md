# EyeViaController (Render-deployable API)

This project started as a local eye-tracking mouse controller using MediaPipe and PyAutoGUI (`eye_mouse.py`).

## ✅ What works in this repo
- Local hardware app: `EyeViaController/eye_mouse.py` (webcam + desktop mouse control)
- Cloud API: `EyeViaController/app.py` (FastAPI endpoints for face landmark extraction)
- Render deployment config: `render.yaml`

## 🚀 Run locally
1. Install dependencies:
   ```bash
   pip install -r EyeViaController/requirements.txt
   ```
2. Start API server:
   ```bash
   uvicorn EyeViaController.app:app --host 0.0.0.0 --port 8000
   ```
3. Open health endpoint:
   - `http://127.0.0.1:8000/health`

## 📦 API endpoints
- `GET /health` — returns service status
- `POST /landmarks` — upload image file (`multipart/form-data`) to get face landmarks

### Example cURL for landmarks
```bash
curl -X POST "http://127.0.0.1:8000/landmarks" -F "image=@./sample.jpg"
```

## ☁️ Deploy on Render
1. Push this repo to GitHub.
2. In Render, create a **Web Service** using this repo and branch `main`.
3. Set build/start commands (if not auto):
   - Build: `pip install -r EyeViaController/requirements.txt`
   - Start: `uvicorn EyeViaController.app:app --host 0.0.0.0 --port $PORT`
4. Deploy and open `https://<your-service>.onrender.com/health`.

## 💡 Notes
- `eye_mouse.py` cannot run on Render (no webcam or GUI desktop control). Keep it local.
- The API is cloud-safe and supports image upload face landmark processing.
