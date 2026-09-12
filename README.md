# Plant Disease AI

Plant disease analysis application with a FastAPI backend and React/Vite frontend.

## Run locally

Start the backend from the repository root:

```powershell
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Start the frontend from `frontend/plantai/plantai`:

```powershell
npm run dev
```

CNN inference uses `best_model.keras` through `vision_engine/linking_cnn.py`.
