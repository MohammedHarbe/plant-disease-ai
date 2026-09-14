"""FastAPI API gateway for Plant Disease AI.

The vision modules own model loading and inference. This module handles HTTP
uploads, temporary files, response shaping, and errors.
"""

import sys
import os
import tempfile
import base64
from pathlib import Path

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    def load_dotenv(*_args, **_kwargs):
        return False

# Add the repository and assistant subsystem to the import path.
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "ai-assistant"))
load_dotenv(dotenv_path=project_root / ".env")

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import the independent vision model functions.
try:
    from vision_engine.linking_yolo import predict_yolo
except ImportError as e:
    print(f"Warning: Could not import predict_yolo: {e}")
    predict_yolo = None

try:
    from vision_engine.linking_cnn import predict_cnn
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",

        # Stable production domain
        "https://plant-disease-ai-1.vercel.app",

        # Current Vercel deployment URL
        "https://plant-disease-ai-1-9tcq8m3is-mohammedharbe.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Only image types the CNN pipeline (PIL) can reliably decode.
_ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/bmp"}
_MAX_UPLOAD_BYTES = 10 * 1024 * 1024


async def _read_image_upload(file: UploadFile) -> bytes:
    if file.content_type not in _ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Uploaded file must be an image (jpeg, png, webp, or bmp).")

    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    if len(contents) > _MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="Uploaded image is too large. Maximum size is 10 MB.")

    return contents


@app.post("/predict/yolo")
async def predict_yolo_endpoint(file: UploadFile = File(...)) -> dict:
    """Run YOLO detection on an uploaded plant image."""
    if predict_yolo is None:
        raise HTTPException(status_code=503, detail="YOLO model is not available on the server.")

    contents = await _read_image_upload(file)

    suffix = Path(file.filename or "").suffix or ".jpg"
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(contents)
            tmp_path = tmp.name

        result = predict_yolo(tmp_path)
        return {
            **result,
            "objectsDetected": result["objects_detected"],
            "healthyRegions": result["healthy_regions"],
            "diseasedRegions": result["diseased_regions"],
            "imageUrl": (
                f"data:{file.content_type};base64,"
                f"{base64.b64encode(contents).decode('ascii')}"
            ),
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="Uploaded file could not be read as an image.")
    except FileNotFoundError:
        print("YOLO prediction error: model or image file not found")
        raise HTTPException(status_code=503, detail="YOLO model is not available on the server.")
    except Exception as error:
        print(f"YOLO prediction error: {error}")
        raise HTTPException(status_code=500, detail="YOLO prediction failed. Please try again.")
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)


@app.post("/predict/cnn")
async def predict_cnn_endpoint(file: UploadFile = File(...)) -> dict:
    """
    CNN classification endpoint.

    Accepts a multipart/form-data image upload (field name "file", which is
    what frontend/.../services/api.ts sends), saves it to a temporary file,
    calls vision_engine.linking_cnn.predict_cnn() on that path, and returns the
    resulting dict as JSON - shaped to match the frontend's CnnResult type.
    """
    if predict_cnn is None:
        raise HTTPException(status_code=503, detail="CNN model is not available on the server.")

    contents = await _read_image_upload(file)

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


class ChatRequest(BaseModel):
    message: str
    context: dict | None = None


@app.post("/chat")
def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    try:
        from gemini_client import generate_response
        answer = generate_response(request.message.strip(), request.context)
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error))
    except Exception as error:
        print(f"Gemini error: {type(error).__name__}: {error}")
        raise HTTPException(
            status_code=502,
            detail="The AI assistant is temporarily unavailable."
        )

    return {"response": answer}


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
