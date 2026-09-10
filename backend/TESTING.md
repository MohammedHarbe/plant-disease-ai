# Backend Testing Guide

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install test dependencies:**
   ```bash
   pip install pytest
   ```

## Running the Backend

### Option 1: Run the server
```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`
- Interactive API docs (Swagger UI): `http://localhost:8000/docs`
- Alternative API docs (ReDoc): `http://localhost:8000/redoc`

### Option 2: Run tests
```bash
pytest test_main.py -v
```

## Testing the Endpoints

### Method 1: Using cURL

**Home endpoint:**
```bash
curl http://localhost:8000/
```

**Health check:**
```bash
curl http://localhost:8000/health
```

**Get diseases:**
```bash
curl http://localhost:8000/diseases
```

**Predict (with file):**
```bash
curl -X POST -F "file=@/path/to/image.jpg" http://localhost:8000/predict
```

### Method 2: Using Python requests
```python
import requests

# Test home
response = requests.get("http://localhost:8000/")
print(response.json())

# Test health
response = requests.get("http://localhost:8000/health")
print(response.json())

# Test diseases
response = requests.get("http://localhost:8000/diseases")
print(response.json())

# Test predict with file
with open("image.jpg", "rb") as f:
    response = requests.post("http://localhost:8000/predict", files={"file": f})
    print(response.json())
```

### Method 3: Using Swagger UI
Simply navigate to `http://localhost:8000/docs` after starting the server to test endpoints interactively.
