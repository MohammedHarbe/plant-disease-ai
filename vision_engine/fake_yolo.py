"""
Fake YOLO model for object detection.

This module simulates YOLO inference for plant disease detection
with bounding boxes, confidence scores, and region analysis.

ARCHITECTURE:
- This is a subsystem independent of FastAPI
- FastAPI will later import and call functions from this module
- The actual YOLO implementation logic goes here
"""


def predict_yolo(image_path: str) -> dict:
    """
    Simulate YOLO object detection.

    Args:
        image_path: Path to the input plant image.

    Returns:
        Dictionary containing fake detection results.
    """

    result = {
        "plant": "Tomato",
        "disease": "Early Blight",
        "confidence": 0.947,
        "severity": "Moderate",

        "objects_detected": 2,
        "healthy_regions": 1,
        "diseased_regions": 1,

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

        "image_path": image_path
    }

    return result
