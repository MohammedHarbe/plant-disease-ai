"""
Test Backend Server - Frontend connects to this
Run with: python test_server.py
Then frontend at api.ts will connect to http://127.0.0.1:8001
"""

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import base64
import io
from PIL import Image
import uvicorn

app = FastAPI(title="Plant Disease API Test Server")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def home():
    """Home endpoint"""
    return {"message": "Plant Disease API Test Server is running"}


@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy"}


@app.get("/diseases")
async def get_diseases():
    """Get list of diseases"""
    return {
        "diseases": [
            "Tomato Early Blight",
            "Tomato Late Blight",
            "Tomato Healthy"
        ]
    }


@app.get("/models")
async def get_models():
    """Get available ML models"""
    return {
        "models": [
            {
                "name": "yolo",
                "description": "YOLOv8 - Object detection with bounding boxes"
            },
            {
                "name": "cnn",
                "description": "CNN - Image classification"
            }
        ]
    }


@app.post("/predict/yolo")
async def predict_yolo(file: UploadFile = File(...)):
    """YOLO Detection endpoint - Frontend sends image here"""
    try:
        # Read uploaded file
        contents = await file.read()
        
        # Convert to base64 for response
        image_base64 = base64.b64encode(contents).decode('utf-8')
        image_url = f"data:image/jpeg;base64,{image_base64}"
        
        # Return mock YOLO detection results
        return JSONResponse({
            "plant": "Tomato",
            "disease": "Early Blight",
            "confidence": 0.947,
            "severity": "Moderate",
            "objectsDetected": 2,
            "healthyRegions": 1,
            "diseasedRegions": 1,
            "detections": [
                {
                    "label": "Diseased leaf",
                    "confidence": 0.947,
                    "x": 16,
                    "y": 23,
                    "width": 38,
                    "height": 29,
                    "status": "diseased"
                },
                {
                    "label": "Healthy leaf",
                    "confidence": 0.873,
                    "x": 55,
                    "y": 48,
                    "width": 27,
                    "height": 23,
                    "status": "healthy"
                }
            ],
            "imageUrl": image_url,
            "inferenceMs": 84
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@app.post("/predict/cnn")
async def predict_cnn(file: UploadFile = File(...)):
    """CNN Classification endpoint - Frontend sends image here"""
    try:
        # Read uploaded file
        contents = await file.read()
        
        # Convert to base64 for response
        image_base64 = base64.b64encode(contents).decode('utf-8')
        image_url = f"data:image/jpeg;base64,{image_base64}"
        
        # Return mock CNN classification results
        return JSONResponse({
            "plant": "Tomato",
            "disease": "Early Blight",
            "confidence": 0.924,
            "predictions": [
                {
                    "label": "Early Blight",
                    "confidence": 0.924
                },
                {
                    "label": "Late Blight",
                    "confidence": 0.048
                },
                {
                    "label": "Healthy",
                    "confidence": 0.028
                }
            ],
            "imageUrl": image_url,
            "inferenceMs": 132
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


if __name__ == "__main__":
    print("🚀 Starting Test Backend Server on http://127.0.0.1:8001")
    print("Frontend api.ts will connect here")
    uvicorn.run(app, host="127.0.0.1", port=8001)
