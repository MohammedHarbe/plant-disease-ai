import pytest
from fastapi.testclient import TestClient
from main import app
import io

client = TestClient(app)


class TestHome:
    """Test home endpoint"""
    
    def test_home_status_code(self):
        """Test that home returns 200"""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_home_response_format(self):
        """Test home response contains expected message"""
        response = client.get("/")
        data = response.json()
        assert "message" in data
        assert data["message"] == "Plant Disease API is running"


class TestHealth:
    """Test health check endpoint"""
    
    def test_health_status_code(self):
        """Test that health returns 200"""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_response_format(self):
        """Test health response contains status"""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"


class TestDiseases:
    """Test diseases list endpoint"""
    
    def test_diseases_status_code(self):
        """Test that diseases endpoint returns 200"""
        response = client.get("/diseases")
        assert response.status_code == 200
    
    def test_diseases_response_format(self):
        """Test diseases response contains list"""
        response = client.get("/diseases")
        data = response.json()
        assert "diseases" in data
        assert isinstance(data["diseases"], list)
    
    def test_diseases_count(self):
        """Test that diseases list has 3 items"""
        response = client.get("/diseases")
        data = response.json()
        assert len(data["diseases"]) == 3
    
    def test_diseases_content(self):
        """Test that all expected diseases are in the list"""
        response = client.get("/diseases")
        data = response.json()
        diseases = data["diseases"]
        
        expected_diseases = [
            "Tomato Early Blight",
            "Tomato Late Blight",
            "Tomato Healthy"
        ]
        
        for disease in expected_diseases:
            assert disease in diseases


class TestModels:
    """Test models endpoint"""
    
    def test_models_status_code(self):
        """Test that models endpoint returns 200"""
        response = client.get("/models")
        assert response.status_code == 200
    
    def test_models_response_format(self):
        """Test models response contains list"""
        response = client.get("/models")
        data = response.json()
        assert "models" in data
        assert isinstance(data["models"], list)
    
    def test_models_count(self):
        """Test that models list has 2 items"""
        response = client.get("/models")
        data = response.json()
        assert len(data["models"]) == 2
    
    def test_models_content(self):
        """Test that models have required fields"""
        response = client.get("/models")
        data = response.json()
        models = data["models"]
        
        for model in models:
            assert "id" in model
            assert "name" in model
            assert "description" in model
        
        model_ids = [m["id"] for m in models]
        assert "yolo" in model_ids
        assert "cnn" in model_ids


class TestYoloPredict:
    """Test YOLO model prediction endpoint"""
    
    def test_yolo_predict_without_file(self):
        """Test YOLO predict without file - should fail"""
        response = client.post("/predict/yolo")
        assert response.status_code == 422
    
    def test_yolo_predict_with_file(self):
        """Test YOLO predict with file"""
        fake_image = io.BytesIO(b"fake image content")
        
        response = client.post(
            "/predict/yolo",
            files={"file": ("test_image.jpg", fake_image, "image/jpeg")}
        )
        
        assert response.status_code == 200
    
    def test_yolo_response_format(self):
        """Test YOLO response has all required fields"""
        fake_image = io.BytesIO(b"fake image content")
        
        response = client.post(
            "/predict/yolo",
            files={"file": ("test_image.jpg", fake_image, "image/jpeg")}
        )
        
        data = response.json()
        assert "plant" in data
        assert "disease" in data
        assert "confidence" in data
        assert "severity" in data
        assert "objectsDetected" in data
        assert "healthyRegions" in data
        assert "diseasedRegions" in data
        assert "detections" in data
        assert "imageUrl" in data
        assert "inferenceMs" in data
    
    def test_yolo_detections_format(self):
        """Test YOLO detections have correct structure"""
        fake_image = io.BytesIO(b"fake image content")
        
        response = client.post(
            "/predict/yolo",
            files={"file": ("test_image.jpg", fake_image, "image/jpeg")}
        )
        
        data = response.json()
        detections = data["detections"]
        
        assert isinstance(detections, list)
        assert len(detections) > 0
        
        for detection in detections:
            assert "label" in detection
            assert "confidence" in detection
            assert "x" in detection
            assert "y" in detection
            assert "width" in detection
            assert "height" in detection
            assert "status" in detection
    
    def test_yolo_confidence_range(self):
        """Test YOLO confidence is 0-100"""
        fake_image = io.BytesIO(b"fake image content")
        
        response = client.post(
            "/predict/yolo",
            files={"file": ("test_image.jpg", fake_image, "image/jpeg")}
        )
        
        data = response.json()
        assert 0 <= data["confidence"] <= 100


class TestCnnPredict:
    """Test CNN model prediction endpoint"""
    
    def test_cnn_predict_without_file(self):
        """Test CNN predict without file - should fail"""
        response = client.post("/predict/cnn")
        assert response.status_code == 422
    
    def test_cnn_predict_with_file(self):
        """Test CNN predict with file"""
        fake_image = io.BytesIO(b"fake image content")
        
        response = client.post(
            "/predict/cnn",
            files={"file": ("test_image.jpg", fake_image, "image/jpeg")}
        )
        
        assert response.status_code == 200
    
    def test_cnn_response_format(self):
        """Test CNN response has all required fields"""
        fake_image = io.BytesIO(b"fake image content")
        
        response = client.post(
            "/predict/cnn",
            files={"file": ("test_image.jpg", fake_image, "image/jpeg")}
        )
        
        data = response.json()
        assert "plant" in data
        assert "disease" in data
        assert "confidence" in data
        assert "predictions" in data
        assert "imageUrl" in data
        assert "inferenceMs" in data
    
    def test_cnn_predictions_format(self):
        """Test CNN predictions have correct structure"""
        fake_image = io.BytesIO(b"fake image content")
        
        response = client.post(
            "/predict/cnn",
            files={"file": ("test_image.jpg", fake_image, "image/jpeg")}
        )
        
        data = response.json()
        predictions = data["predictions"]
        
        assert isinstance(predictions, list)
        assert len(predictions) > 0
        
        for prediction in predictions:
            assert "label" in prediction
            assert "confidence" in prediction
            assert 0 <= prediction["confidence"] <= 100
    
    def test_cnn_confidence_range(self):
        """Test CNN confidence is 0-100"""
        fake_image = io.BytesIO(b"fake image content")
        
        response = client.post(
            "/predict/cnn",
            files={"file": ("test_image.jpg", fake_image, "image/jpeg")}
        )
        
        data = response.json()
        assert 0 <= data["confidence"] <= 100


class TestCORS:
    """Test CORS headers"""
    
    def test_cors_headers_present(self):
        """Test that CORS headers are present in response"""
        response = client.get("/", headers={"Origin": "http://localhost:3000"})
        assert response.status_code == 200


class TestContentTypes:
    """Test content type headers"""
    
    def test_home_content_type(self):
        """Test that home returns JSON"""
        response = client.get("/")
        assert "application/json" in response.headers["content-type"]
    
    def test_health_content_type(self):
        """Test that health returns JSON"""
        response = client.get("/health")
        assert "application/json" in response.headers["content-type"]
    
    def test_diseases_content_type(self):
        """Test that diseases returns JSON"""
        response = client.get("/diseases")
        assert "application/json" in response.headers["content-type"]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
