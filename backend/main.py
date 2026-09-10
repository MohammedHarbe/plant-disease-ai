from fastapi import FastAPI, UploadFile, File, HTTPException

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Plant Disease API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # 1. Check file
    # 2. Read image
    # 3. Preprocess image
    # 4. Give image to ML model
    # 5. Get prediction
    # 6. Return result

    return {
        "disease": "Tomato Late Blight",
        "confidence": 94.2
    }


@app.get("/diseases")
def get_diseases():
    return {
        "diseases": [
            "Tomato Early Blight",
            "Tomato Late Blight",
            "Tomato Healthy"
        ]
    }
