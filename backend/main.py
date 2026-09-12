"""
FastAPI application entry point for Plant Disease AI.

This module defines the FastAPI application and will eventually contain
HTTP endpoints that call functions from the vision-engine and ai-assistant subsystems.

ARCHITECTURE NOTE:
- FastAPI here is ONLY the API layer/gateway
- The vision-engine and ai-assistant are independent subsystems in their own folders
- We will later import from those modules and call their functions in these endpoints
- Do NOT put model implementation logic here
- Do NOT put AI logic here

TODO: Add these endpoints (do not implement yet):
  1. POST /predict/yolo - Call vision-engine.fake_yolo.predict_yolo()
  2. POST /predict/cnn - Call vision-engine.fake_cnn.predict_cnn()
  3. POST /assistant/ask - Call ai-assistant.fake_assistant.answer_question()
"""

import sys
import os
import tempfile
import base64
from pathlib import Path

# Add project root to path so we can import vision_engine and ai-assistant
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from pydantic import BaseModel
from google.genai import types

# Import the fake model functions
try:
    from vision_engine.fake_yolo import predict_yolo
except ImportError as e:
    print(f"Warning: Could not import predict_yolo: {e}")
    predict_yolo = None

try:
    from vision_engine.fake_cnn import predict_cnn
except ImportError as e:
    print(f"Warning: Could not import predict_cnn: {e}")
    predict_cnn = None

# Create FastAPI application
app = FastAPI(
    title="Plant Disease AI Backend",
    description="API gateway for plant disease detection and AI assistance",
    version="0.1.0"
)

# ============================================================================
# CORS
# ============================================================================
# The React/Vite frontend (frontend/plantai/plantai) runs on its own dev
# server (Vite's default port 5173), separate from this FastAPI process
# (uvicorn, default port 8000). Browsers block cross-origin fetch() calls
# by default ("CORS" = Cross-Origin Resource Sharing), so without this
# middleware the browser would reject every request api.ts makes to
# http://127.0.0.1:8000 from a page served on http://localhost:5173, even
# though the request itself would have worked fine. We list the exact
# Vite dev origins (from vite.config.ts, which uses Vite's default port)
# instead of "*", since "*" would allow any website on the internet to call
# this API from a user's browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Only image types the CNN pipeline (PIL) can reliably decode.
_ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/bmp"}


# ============================================================================
# FUTURE ENDPOINTS (Do NOT implement yet)
# ============================================================================

# TODO: @app.post("/predict/yolo")
# async def predict_yolo(file: UploadFile = File(...)) -> dict:
#     """
#     YOLO object detection endpoint.
#     
#     Will eventually:
#     - Accept an image file
#     - Call vision_engine.fake_yolo.predict_yolo()
#     - Return detections with bounding boxes
#     """
#     pass

SYSTEM_MESSAGE_PATH = "system_message.txt"

@app.get("/predict/yolo")
def test_yolo():
    """Test endpoint for YOLO prediction."""
    if predict_yolo is None:
        return {"error": "YOLO model not loaded", "status": "import failed"}
    
    result = predict_yolo("test_image.jpg")
    return result


@app.post("/predict/cnn")
async def predict_cnn_endpoint(file: UploadFile = File(...)) -> dict:
    """
    CNN classification endpoint.

    Accepts a multipart/form-data image upload (field name "file", which is
    what frontend/.../services/api.ts sends), saves it to a temporary file,
    calls vision_engine.fake_cnn.predict_cnn() on that path, and returns the
    resulting dict as JSON - shaped to match the frontend's CnnResult type.
    """
    if predict_cnn is None:
        raise HTTPException(status_code=503, detail="CNN model is not available on the server.")

    if file.content_type not in _ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file must be an image (jpeg, png, webp, or bmp).",
        )

    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    suffix = Path(file.filename or "").suffix or ".jpg"
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(contents)
            tmp_path = tmp.name

        result = predict_cnn(tmp_path)
        # Keep the original upload available to the frontend result view.
        result["imageUrl"] = (
            f"data:{file.content_type};base64,"
            f"{base64.b64encode(contents).decode('ascii')}"
        )
        return result

    except ValueError:
        # Raised by predict_cnn() when PIL can't decode the file as an image.
        raise HTTPException(status_code=400, detail="Uploaded file could not be read as an image.")
    except FileNotFoundError:
        # Raised by predict_cnn() when best_model.keras is missing.
        print(f"CNN prediction error: model file not found")  # server-side log only
        raise HTTPException(status_code=500, detail="CNN model is not available on the server.")
    except Exception as e:
        # Never leak stack traces or filesystem paths to the client.
        print(f"CNN prediction error: {e}")  # server-side log only
        raise HTTPException(status_code=500, detail="CNN prediction failed. Please try again.")
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"message": "Plant Assistant is running"}


@app.post("/chat")
def chat(request: ChatRequest):
    print("Sending request to Gemini...")

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=request.message,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_MESSAGE_PATH ,
            temperature=0.2,
            max_output_tokens=200,
        )
    )

    print("Gemini response received!")    

    return {"response": response.text}


# ============================================================================
# OPTIONAL: Simple verification endpoints
# ============================================================================

# Optional: Remove these once you start implementing real endpoints
@app.get("/")
def root():
    """Root endpoint - verify FastAPI is running."""
    return {
        "message": "Plant Disease AI Backend is running",
        "status": "ready for implementation"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# ============================================================================
# STARTUP/SHUTDOWN EVENTS (for future use)
# ============================================================================

# TODO: You might add startup events here later to:
#  - Load ML models (YOLO, CNN)
#  - Initialize database connections
#  - Set up logging
#  - Load configuration

# @app.on_event("startup")
# async def startup_event():
#     """Initialize resources on startup."""
#     pass


# @app.on_event("shutdown")
# async def shutdown_event():
#     """Clean up resources on shutdown."""
#     pass
