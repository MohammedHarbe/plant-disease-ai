"""
Request and Response schemas for FastAPI endpoints.

These Pydantic models will eventually define:
1. Request formats expected by FastAPI endpoints
2. Response formats returned to the frontend
3. Data validation rules

TODO: Create these schemas (do not implement yet):

1. YOLO Prediction Response:
   - disease (str)
   - confidence (float)
   - severity (str)
   - detections (list of detection objects)
   - inference_ms (int)
   - image_base64 (str)

2. CNN Prediction Response:
   - predictions (list of prediction objects)
   - confidence (float)
   - disease (str)
   - inference_ms (int)
   - image_base64 (str)

3. Assistant Request:
   - question (str)
   - context (dict, optional)

4. Assistant Response:
   - answer (str)
   - confidence (float, optional)

EXAMPLE (do not implement yet):

from pydantic import BaseModel
from typing import List, Optional

class YoloDetection(BaseModel):
    label: str
    confidence: float
    x: int
    y: int
    width: int
    height: int
    status: str  # "healthy" or "diseased"

class YoloPredictionResponse(BaseModel):
    plant: str
    disease: str
    confidence: float
    severity: str
    detections: List[YoloDetection]
    inference_ms: int
    image_base64: str
"""

# Placeholder - Schemas will be added as you implement endpoints
