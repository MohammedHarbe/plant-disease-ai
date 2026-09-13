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

## Deploy Frontend On Vercel

Deploy the React/Vite frontend as a Vercel project.

Vercel settings:

```text
Framework Preset: Vite
Root Directory: frontend/plantai/plantai
Build Command: npm run build
Output Directory: dist
Environment Variable: VITE_API_URL=https://your-backend-url
```

The frontend uses React Router, so `frontend/plantai/plantai/vercel.json` rewrites all routes to `index.html`. Refreshing routes such as `/analyze`, `/results/yolo`, `/compare`, `/assistant`, and `/history` should work on Vercel.

`VITE_API_URL` should point to the deployed FastAPI backend. Do not put `API_KEY` or any other backend secret in Vercel frontend variables.

## Backend Hosting

Keep the FastAPI backend as a separate web service on Render or another backend host.

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
FRONTEND_ORIGIN=https://your-vercel-domain.vercel.app
```

`API_KEY` belongs only on the backend service. The backend CORS configuration allows localhost development origins and the single production origin from `FRONTEND_ORIGIN`.

The root `render.yaml` is now backend-only and can be used later if you choose Render for the API service. The frontend should be deployed from Vercel.

### Deployment Order

1. Deploy the backend service on your chosen backend host.
2. Copy the backend URL.
3. In Vercel, set frontend `VITE_API_URL` to the backend URL.
4. Deploy the frontend on Vercel.
5. Copy the Vercel frontend URL.
6. Set backend `FRONTEND_ORIGIN` to the Vercel URL, for example `https://plantai.vercel.app`.
7. Redeploy or restart the backend so production CORS uses the final Vercel origin.
