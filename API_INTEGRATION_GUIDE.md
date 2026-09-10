# Plant Disease AI - Backend & Frontend Integration Guide

## 🎯 API Overview

The backend now provides two ML model prediction endpoints to match the React frontend requirements:

### **Base URL**: `http://127.0.0.1:8000`

---

## 📡 API Endpoints

### 1. **GET `/`** - Home
Returns API status message.

**Response:**
```json
{
  "message": "Plant Disease API is running"
}
```

---

### 2. **GET `/health`** - Health Check
Verify API is running.

**Response:**
```json
{
  "status": "healthy"
}
```

---

### 3. **GET `/diseases`** - List All Diseases
Get all detectable plant diseases.

**Response:**
```json
{
  "diseases": [
    "Tomato Early Blight",
    "Tomato Late Blight",
    "Tomato Healthy"
  ]
}
```

---

### 4. **GET `/models`** - List Available Models
Get all available prediction models.

**Response:**
```json
{
  "models": [
    {
      "id": "yolo",
      "name": "YOLO (Real-time Detection)",
      "description": "Fast object detection with bounding boxes"
    },
    {
      "id": "cnn",
      "name": "CNN (Classification)",
      "description": "Accurate image classification"
    }
  ]
}
```

---

### 5. **POST `/predict/yolo`** - YOLO Object Detection
Upload an image for YOLO object detection with bounding boxes.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: Image file in `file` parameter

**Response:**
```json
{
  "plant": "Tomato",
  "disease": "Tomato Early Blight",
  "confidence": 92.5,
  "severity": "moderate",
  "objectsDetected": 3,
  "healthyRegions": 2,
  "diseasedRegions": 1,
  "detections": [
    {
      "label": "blight",
      "confidence": 92.5,
      "x": 150,
      "y": 120,
      "width": 200,
      "height": 180,
      "status": "diseased"
    },
    {
      "label": "healthy_leaf",
      "confidence": 95.0,
      "x": 400,
      "y": 100,
      "width": 150,
      "height": 140,
      "status": "healthy"
    }
  ],
  "imageUrl": "data:image/jpeg;base64,...",
  "inferenceMs": 185
}
```

---

### 6. **POST `/predict/cnn`** - CNN Classification
Upload an image for CNN classification.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: Image file in `file` parameter

**Response:**
```json
{
  "plant": "Tomato",
  "disease": "Tomato Early Blight",
  "confidence": 94.2,
  "predictions": [
    {
      "label": "Tomato Early Blight",
      "confidence": 94.2
    },
    {
      "label": "Tomato Late Blight",
      "confidence": 3.8
    },
    {
      "label": "Tomato Healthy",
      "confidence": 2.0
    }
  ],
  "imageUrl": "data:image/jpeg;base64,...",
  "inferenceMs": 156
}
```

---

## 🔗 Frontend Integration

The frontend (React/TypeScript app) is configured to use these endpoints:

### **API Service Configuration**
File: `frontend/plantai/plantai/src/services/api.ts`

```typescript
const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';

export async function predictYolo(imageUrl: string): Promise<YoloResult>
export async function predictCnn(imageUrl: string): Promise<CnnResult>
export async function askPlantAI(message: string): Promise<string>
```

### **Environment Variables**
Create `.env` file in frontend directory:
```
REACT_APP_API_URL=http://127.0.0.1:8000
```

---

## 🚀 Running the System

### **Terminal 1: Start Backend**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### **Terminal 2: Start Frontend**
```bash
cd frontend/plantai/plantai
npm install
npm run dev
```

### **Backend Tests**
```bash
cd backend
pytest test_api.py -v
```

---

## ✅ Test Results

**Total Tests:** 26
- ✅ Home Endpoint: 2 tests
- ✅ Health Check: 2 tests
- ✅ Diseases List: 4 tests
- ✅ Models List: 4 tests
- ✅ YOLO Prediction: 5 tests
- ✅ CNN Prediction: 5 tests
- ✅ CORS: 1 test
- ✅ Content Types: 3 tests

**Status:** 26/26 PASSED ✅

---

## 📊 Data Type Definitions

### **YoloResult** (Frontend Type)
```typescript
{
  plant: string;
  disease: string;
  confidence: number;
  severity: string;
  objectsDetected: number;
  healthyRegions: number;
  diseasedRegions: number;
  detections: Detection[];
  imageUrl: string;
  inferenceMs: number;
}
```

### **CnnResult** (Frontend Type)
```typescript
{
  plant: string;
  disease: string;
  confidence: number;
  predictions: CnnPrediction[];
  imageUrl: string;
  inferenceMs: number;
}
```

### **Detection** (Frontend Type)
```typescript
{
  label: string;
  confidence: number;
  x: number;
  y: number;
  width: number;
  height: number;
  status: 'healthy' | 'diseased';
}
```

### **CnnPrediction** (Frontend Type)
```typescript
{
  label: string;
  confidence: number;
}
```

---

## 🔒 CORS Configuration

CORS is enabled for all origins (development):
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

For production, restrict to your frontend domain:
```python
allow_origins=["https://yourdomain.com"]
```

---

## 📝 API Testing

### **Option 1: Automated Tests**
```bash
cd backend
pytest test_api.py -v
```

### **Option 2: Interactive HTML UI**
Open `backend/test_api.html` in browser

### **Option 3: Swagger UI**
Visit: `http://127.0.0.1:8000/docs`

### **Option 4: cURL**
```bash
# YOLO Prediction
curl -X POST -F "file=@image.jpg" http://127.0.0.1:8000/predict/yolo

# CNN Prediction
curl -X POST -F "file=@image.jpg" http://127.0.0.1:8000/predict/cnn
```

### **Option 5: Python**
```python
import requests

with open('image.jpg', 'rb') as f:
    response = requests.post(
        'http://127.0.0.1:8000/predict/yolo',
        files={'file': f}
    )
    print(response.json())
```

---

## 🛠️ Project Structure

```
plant-disease-ai/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── test_api.py             # Pytest test suite (26 tests)
│   ├── test_api.html           # Interactive web UI tests
│   ├── requirements.txt        # Python dependencies
│   └── TESTING.md              # Testing documentation
│
└── frontend/
    └── plantai/plantai/
        ├── src/
        │   ├── services/
        │   │   └── api.ts      # API integration layer
        │   ├── pages/
        │   │   ├── Analyze.tsx # Image upload page
        │   │   ├── Results.tsx # Prediction results
        │   │   └── ...
        │   └── types/
        │       └── index.ts    # TypeScript types
        ├── package.json
        └── .env                # API URL configuration
```

---

## 🎯 Next Steps

1. **Implement Real ML Models**
   - Replace mock predictions with actual YOLO model
   - Replace mock predictions with actual CNN model
   - Use TensorFlow, PyTorch, or OpenCV

2. **Database Integration**
   - Store prediction history
   - User authentication
   - Plant disease database

3. **Production Deployment**
   - Deploy backend (AWS, Heroku, DigitalOcean)
   - Deploy frontend (Vercel, Netlify)
   - Update CORS for production domain
   - Use environment variables for API URL

4. **Enhanced Features**
   - Real plant-specific AI assistant
   - Disease recommendations and treatment guides
   - Image comparison and history

---

## ✨ Summary

✅ Backend API fully matches frontend requirements
✅ All 26 tests passing
✅ CORS enabled for cross-origin requests
✅ Support for both YOLO (detection) and CNN (classification) models
✅ Image base64 encoding/decoding built-in
✅ Ready for real model integration
