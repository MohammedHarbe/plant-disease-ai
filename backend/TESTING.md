# Plant Disease API - Testing Guide

## Quick Start

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Start the API Server
```bash
uvicorn main:app --reload --port 8000
```

The API will be available at: `http://127.0.0.1:8000`

---

## Testing Methods

### Method 1: Automated Tests (pytest)

Run all tests:
```bash
cd backend
pytest test_api.py -v
```

Run specific test class:
```bash
pytest test_api.py::TestHealth -v
```

Run with coverage report:
```bash
pytest test_api.py --cov=main
```

### Method 2: Interactive HTML Test Suite

1. Open `test_api.html` in your browser (or navigate to the file)
2. API URL is pre-configured to `http://127.0.0.1:8000`
3. Click individual test buttons or "Run All Tests"
4. View responses and CORS headers

### Method 3: cURL Commands

**Health Check:**
```bash
curl http://127.0.0.1:8000/health
```

**Get Diseases:**
```bash
curl http://127.0.0.1:8000/diseases
```

**Predict (with image):**
```bash
curl -X POST -F "file=@image.jpg" http://127.0.0.1:8000/predict
```

### Method 4: Python Requests

```python
import requests

# Health
response = requests.get('http://127.0.0.1:8000/health')
print(response.json())

# Diseases
response = requests.get('http://127.0.0.1:8000/diseases')
print(response.json())

# Predict
with open('image.jpg', 'rb') as f:
    response = requests.post(
        'http://127.0.0.1:8000/predict',
        files={'file': f}
    )
    print(response.json())
```

### Method 5: Swagger UI

Visit: `http://127.0.0.1:8000/docs`

This gives you an interactive API documentation where you can:
- Test all endpoints
- Upload files
- See response schemas

---

## API Endpoints

| Endpoint | Method | Description | Response |
|----------|--------|-------------|----------|
| `/` | GET | Home message | `{"message": "Plant Disease API is running"}` |
| `/health` | GET | Health check | `{"status": "healthy"}` |
| `/diseases` | GET | List all diseases | `{"diseases": ["Tomato Early Blight", ...]}` |
| `/predict` | POST | Predict disease from image | `{"disease": "Tomato Late Blight", "confidence": 94.2}` |

---

## Test Categories

### Home Endpoint Tests
- Status code validation (200)
- Response format validation
- Message content verification

### Health Check Tests
- Status code validation (200)
- Response format validation
- Status field verification

### Diseases List Tests
- Status code validation (200)
- Response format validation
- List count verification
- Content verification

### Predict Endpoint Tests
- Missing file validation (422 error)
- File upload success (200)
- Response format validation
- Response values validation
- Confidence range validation (0-100)
- Different file types (JPG, PNG, GIF)

### CORS Tests
- CORS headers presence
- Origin validation

### Content Type Tests
- JSON content type validation for all endpoints

---

## Expected Test Results

All tests should pass with:
- ✅ Status code 200 for successful requests
- ✅ Status code 422 for missing required file
- ✅ Valid JSON responses
- ✅ CORS headers configured
- ✅ Proper content-type headers

---

## Troubleshooting

**API is offline?**
- Make sure backend is running: `uvicorn main:app --reload --port 8000`
- Check if port 8000 is already in use

**Tests are failing?**
- Check the detailed error message in test output
- Verify API responses in Swagger UI: `http://127.0.0.1:8000/docs`
- Check CORS configuration in `main.py`

**File upload not working?**
- Ensure `python-multipart` is installed
- Check that file parameter name is correct: `file`

---

## Test Summary

This test suite provides:
- ✅ 20+ unit and integration tests
- ✅ Interactive HTML test UI
- ✅ Automated pytest execution
- ✅ CORS validation
- ✅ File upload testing
- ✅ Response format validation
