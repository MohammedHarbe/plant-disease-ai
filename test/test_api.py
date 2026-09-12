import io
import asyncio
from pathlib import Path

import httpx

from backend.main import app


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEST_IMAGE = PROJECT_ROOT / "test" / "_test_green.jpg"


def request(method: str, path: str, **kwargs) -> httpx.Response:
    async def send_request() -> httpx.Response:
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://testserver",
        ) as client:
            return await client.request(method, path, **kwargs)

    return asyncio.run(send_request())


def test_home_and_health():
    assert request("GET", "/").status_code == 200
    assert request("GET", "/health").json() == {"status": "healthy"}


def test_yolo_requires_file():
    assert request("POST", "/predict/yolo").status_code == 422


def test_yolo_accepts_real_image():
    response = request(
        "POST",
        "/predict/yolo",
        files={"file": ("test.jpg", TEST_IMAGE.read_bytes(), "image/jpeg")},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["detection_count"] == len(body["detections"])
    assert body["inference_time_ms"] >= 0
    assert body["imageUrl"].startswith("data:image/jpeg;base64,")


def test_yolo_rejects_corrupt_image():
    response = request(
        "/predict/yolo",
        files={"file": ("bad.jpg", io.BytesIO(b"not an image"), "image/jpeg")},
    )

    assert response.status_code == 400


def test_cnn_accepts_real_image():
    response = request(
        "POST",
        "/predict/cnn",
        files={"file": ("test.jpg", TEST_IMAGE.read_bytes(), "image/jpeg")},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["predictions"]
    assert body["imageUrl"].startswith("data:image/jpeg;base64,")
