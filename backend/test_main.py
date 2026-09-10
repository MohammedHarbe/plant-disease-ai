import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    """Test the home endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Plant Disease API is running"}


def test_health():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_diseases():
    """Test the diseases list endpoint"""
    response = client.get("/diseases")
    assert response.status_code == 200
    data = response.json()
    assert "diseases" in data
    assert len(data["diseases"]) == 3
    assert "Tomato Early Blight" in data["diseases"]
    assert "Tomato Late Blight" in data["diseases"]
    assert "Tomato Healthy" in data["diseases"]


def test_predict_no_file():
    """Test predict endpoint without file"""
    response = client.post("/predict")
    assert response.status_code == 422  # Validation error - file required


def test_predict_with_file():
    """Test predict endpoint with a file"""
    with open("test_image.jpg", "wb") as f:
        f.write(b"fake image content")
    
    with open("test_image.jpg", "rb") as f:
        response = client.post("/predict", files={"file": f})
    
    assert response.status_code == 200
    data = response.json()
    assert "disease" in data
    assert "confidence" in data
    assert data["disease"] == "Tomato Late Blight"
    assert data["confidence"] == 94.2
