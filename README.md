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

YOLO model: `yolo.pt`

YOLO inference: `vision_engine/linking_yolo.py`

CNN inference: `vision_engine/linking_cnn.py`

## Deploy On Render

This repo includes a root-level `render.yaml` blueprint with:

- Backend Web Service: `plantai-api`
- Frontend Static Site: `plantai-web`

### Backend

Service type: Render Web Service

Root directory: repository root

Build command:

```bash
pip install -r backend/requirements.txt
```

Start command:

```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

Health check path:

```text
/health
```

Required backend environment variables:

```text
API_KEY=your Gemini API key
FRONTEND_ORIGIN=https://your-frontend.onrender.com
PYTHON_VERSION=3.11.9
```

`API_KEY` belongs only on the backend service. Do not expose it through `VITE_*` variables or frontend code.

### Frontend

Service type: Render Static Site

Root directory:

```text
frontend/plantai/plantai
```

Build command:

```bash
npm install && npm run build
```

Publish directory:

```text
dist
```

Required frontend environment variable:

```text
VITE_API_URL=https://your-backend.onrender.com
```

The blueprint also configures React Router SPA refresh support with:

```text
/* -> /index.html
```

### Deployment Order

1. Deploy the backend service.
2. Copy the backend Render URL.
3. Set the frontend `VITE_API_URL` to the backend URL.
4. Deploy the frontend static site.
5. Copy the frontend Render URL.
6. Set the backend `FRONTEND_ORIGIN` to the frontend URL.
7. Redeploy the backend so production CORS uses the final frontend origin.

The blueprint creates the service shapes, but you still need to set real Render URLs and the real backend-only `API_KEY` in Render.
