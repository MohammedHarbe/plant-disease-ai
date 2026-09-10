"""
FastAPI Backend for Plant Disease AI.

This is the API layer/gateway that exposes the vision-engine and ai-assistant
subsystems through HTTP endpoints.

ARCHITECTURE:
- FastAPI is ONLY the HTTP API layer
- Vision engine subsystem (fake_yolo.py, fake_cnn.py) is independent
- AI assistant subsystem (fake_assistant.py) is independent
- This module imports and calls functions from those subsystems

Future flow:
  Frontend (HTTP request)
    |
    v
  FastAPI endpoint (main.py)
    |
    v
  Vision-engine or AI-assistant subsystem
    |
    v
  Result back to FastAPI
    |
    v
  JSON response to frontend
"""
