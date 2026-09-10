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

from fastapi import FastAPI

# Create FastAPI application
app = FastAPI(
    title="Plant Disease AI Backend",
    description="API gateway for plant disease detection and AI assistance",
    version="0.1.0"
)


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


# TODO: @app.post("/predict/cnn")
# async def predict_cnn(file: UploadFile = File(...)) -> dict:
#     """
#     CNN classification endpoint.
#     
#     Will eventually:
#     - Accept an image file
#     - Call vision_engine.fake_cnn.predict_cnn()
#     - Return top-K predictions
#     """
#     pass


# TODO: @app.post("/assistant/ask")
# async def ask_assistant(question: str, context: dict = None) -> dict:
#     """
#     AI Assistant endpoint.
#     
#     Will eventually:
#     - Accept a question about plant health
#     - Optionally accept context from previous predictions
#     - Call ai_assistant.fake_assistant.answer_question()
#     - Return assistant response
#     """
#     pass


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
