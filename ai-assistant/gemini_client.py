"""Gemini client for the PlantAI assistant subsystem."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SYSTEM_MESSAGE_PATH = PROJECT_ROOT / "ai-assistant" / "system_message.txt"

load_dotenv()
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")

api_key = os.getenv("API_KEY")
if not api_key:
    raise RuntimeError(
        "API_KEY is not configured. Add it to the project root .env file."
    )

client = genai.Client(api_key=api_key)


def generate_response(message: str, context: dict | None = None) -> str:
    """Generate a plant-focused answer without exposing credentials."""
    context_text = ""
    if context:
        context_text = (
            "\n\nThe user is asking about this latest plant analysis result. "
            f"Use it as factual context:\n{context}"
        )

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=f"User question: {message}{context_text}",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_MESSAGE_PATH.read_text(encoding="utf-8"),
            temperature=0.2,
            max_output_tokens=200,
        ),
    )
    return response.text or "I could not generate a response. Please try again."
