
I am building a Plant Disease AI project and I want you to now implement the CNN → FastAPI → Frontend connection.

IMPORTANT: Do not redesign the project architecture. Work with the existing repository and files.

Current architecture:

plant-disease-ai/
│
├── ai_assistant/
│   ├── __init__.py
│   └── fake_assistant.py
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── requirements.txt
│   └── schemas/
│       ├── __init__.py
│       └── requests.py
│
├── vision_engine/
│   ├── __init__.py
│   ├── fake_yolo.py
│   └── fake_cnn.py
│
├── frontend/
│   └── existing React/Vite frontend
│
└── best_model.keras

The frontend already has:
frontend/.../services/api.ts

Its current CNN function sends:

POST /predict/cnn

using multipart/form-data with:

formData.append('file', blob)

The frontend currently has mock fallbacks, but I now want the real CNN → FastAPI connection to work.

==================================================
GOAL
==================================================

Implement this complete flow:

Frontend
   │
   │ HTTP POST /predict/cnn
   │ multipart/form-data
   │ file = image
   ▼
FastAPI
backend/main.py
   │
   │ UploadFile
   ▼
vision_engine/fake_cnn.py
   │
   │ load/use best_model.keras
   ▼
TensorFlow/Keras CNN
   │
   ▼
prediction result
   │
   ▼
FastAPI JSON response
   │
   ▼
Frontend

==================================================
VERY IMPORTANT: INSPECT BEFORE MODIFYING
==================================================

Before making changes:

1. Inspect the existing repository structure.
2. Inspect:
   - vision_engine/fake_cnn.py
   - vision_engine/fake_yolo.py
   - backend/main.py
   - backend/requirements.txt
   - backend/schemas/requests.py
   - frontend/.../services/api.ts
   - frontend/.../types/index.ts
   - the existing frontend analysis/result components
3. Inspect the existing best_model.keras if possible.
4. Determine:
   - model input shape
   - number of output classes
   - output layer structure
   - whether it is a complete Keras model or weights only
5. Do NOT guess the CNN preprocessing.
6. If the repository contains the training notebook/code, inspect it and reproduce the SAME:
   - image size
   - normalization/scaling
   - color format
   - class ordering
   - preprocessing
7. Do not change the frontend UI unnecessarily.

The most important requirement is that inference preprocessing and class mapping match the training process that produced best_model.keras.

==================================================
PART 1 — CNN VISION ENGINE
==================================================

Implement the real CNN inference inside:

vision_engine/fake_cnn.py

You may rename it to:

vision_engine/cnn.py

if that is cleaner, but keep the public function interface simple and explain the change.

The function should conceptually remain:

predict_cnn(image_path: str) -> dict

It should:

1. Load best_model.keras.
2. Load the image.
3. Apply exactly the preprocessing used during training.
4. Run TensorFlow/Keras inference.
5. Convert model output into probabilities.
6. Determine the predicted disease/class.
7. Return a clean Python dictionary.

IMPORTANT:
Do NOT load the model every time predict_cnn() is called if that can be avoided.

Prefer loading the model once when the vision engine starts, or using a module-level cached model.

For example, the architecture should conceptually be:

model = load_model(...)

def predict_cnn(image_path):
    ...
    prediction = model.predict(...)
    ...
    return result

But adapt this to the existing project.

Do not put FastAPI code inside the CNN module.

The vision engine must remain independent of FastAPI.

==================================================
PART 2 — MODEL PATH
==================================================

The trained model currently exists at:

best_model.keras

Do not hard-code a fragile absolute Windows path.

Use a project-relative path, preferably with pathlib, so the project works when launched from the repository root.

For example, determine the correct path using __file__ and pathlib.

Do not move or duplicate the model unless necessary.

==================================================
PART 3 — CNN RESPONSE FORMAT
==================================================

Inspect the existing frontend TypeScript types and make the backend response compatible with them.

The existing frontend expects a CnnResult similar to:

{
    plant: string,
    disease: string,
    confidence: number,
    predictions: [
        {
            label: string,
            confidence: number
        }
    ],
    imageUrl: string,
    inferenceMs: number
}

Do not invent a completely different response structure.

If the existing type differs, use the actual type from the repository.

The CNN should return useful top-K predictions, for example:

{
    "plant": "Tomato",
    "disease": "Early Blight",
    "confidence": 0.924,
    "predictions": [
        {
            "label": "Early Blight",
            "confidence": 0.924
        },
        {
            "label": "Late Blight",
            "confidence: 0.048
        },
        {
            "label": "Healthy",
            "confidence": 0.028
        }
    ],
    "imageUrl": "...",
    "inferenceMs": 132
}

BUT do not blindly use these example values.

Use the actual model's output/classes.

==================================================
PART 4 — FASTAPI
==================================================

Implement:

POST /predict/cnn

in:

backend/main.py

The endpoint must accept:

UploadFile = File(...)

because the frontend sends multipart/form-data.

Use:

python-multipart

which is already intended to be in requirements.txt.

The endpoint should:

1. Receive the uploaded image.
2. Validate that it is an image.
3. Temporarily save it or otherwise make it available to the vision engine.
4. Call:

predict_cnn(image_path)

5. Return the prediction dictionary as JSON.
6. Clean up temporary files if appropriate.

Do NOT put TensorFlow model logic inside main.py.

main.py should only handle API concerns.

Architecture must remain:

FastAPI
   ↓
predict_cnn()
   ↓
vision_engine
   ↓
TensorFlow model

==================================================
PART 5 — MODEL LOADING
==================================================

Make sure TensorFlow/Keras is added to the backend requirements.

Add only the dependencies actually required.

At minimum, determine whether the project needs:

tensorflow
pillow
python-multipart
fastapi
uvicorn

Do not randomly install unnecessary ML libraries such as PyTorch or Ultralytics for the CNN.

Use TensorFlow/Keras because best_model.keras is a Keras model.

If a specific TensorFlow version is required for compatibility with best_model.keras, determine that from the repository/model/training environment instead of guessing.

==================================================
PART 6 — CORS
==================================================

The frontend is running separately from FastAPI during development.

Configure FastAPI CORS correctly for the existing Vite frontend development origin.

Do not use "*" blindly if the existing project already specifies an origin.

Inspect the frontend configuration and determine the correct development origin.

Explain why CORS is needed.

==================================================
PART 7 — FRONTEND
==================================================

Inspect:

frontend/.../services/api.ts

The frontend already attempts:

POST /predict/cnn

with:

FormData
file

Connect this to the real FastAPI endpoint.

Keep the existing function interface:

predictCnn(imageUrl: string): Promise<CnnResult>

if possible.

Do not rewrite the frontend architecture.

Do not redesign the UI.

Only modify what is necessary to:

1. Send the image to FastAPI.
2. Receive the CNN JSON response.
3. Use the real response instead of mock data.

IMPORTANT:
The current code has:

catch {
    return cnnDemo;
}

This can hide backend errors.

For development, change this behavior so that API errors are visible/logged rather than silently making it look like the CNN worked.

However, do not break the application unnecessarily. Explain the change.

==================================================
PART 8 — DO NOT TOUCH YOLO
==================================================

There is already a fake YOLO subsystem.

Do NOT replace or redesign it.

Do NOT install YOLO dependencies just for this task.

Keep:

vision_engine/fake_yolo.py

independent.

The goal right now is:

REAL CNN
+
FastAPI
+
existing frontend

while YOLO remains fake.

==================================================
PART 9 — ERROR HANDLING
==================================================

Add sensible error handling for:

- invalid file type
- missing file
- unreadable/corrupted image
- model loading failure
- prediction failure

Return appropriate HTTP errors from FastAPI.

Do not expose Python stack traces or internal filesystem paths to the frontend.

==================================================
PART 10 — TESTING
==================================================

After implementing, test in this order:

TEST 1:
Run the CNN vision engine directly without FastAPI.

Example concept:

python test_cnn_direct.py

It should prove:

image
 ↓
predict_cnn()
 ↓
best_model.keras
 ↓
prediction dictionary

TEST 2:
Run FastAPI:

uvicorn backend.main:app --reload

TEST 3:
Open:

/docs

and test:

POST /predict/cnn

using the Swagger UI file upload.

TEST 4:
Test the existing frontend and verify:

Frontend
 ↓
POST /predict/cnn
 ↓
FastAPI
 ↓
TensorFlow CNN
 ↓
JSON
 ↓
Frontend result page

==================================================
VERY IMPORTANT — TEACH ME
==================================================

I am using this project to learn backend/FastAPI architecture.

Do NOT just dump code without explanation.

Before editing, briefly explain the architecture you found.

After editing, explain:

1. What changed in fake_cnn.py/cnn.py.
2. How best_model.keras is loaded.
3. How preprocessing works and why it must match training.
4. How the image travels from React to FastAPI.
5. How UploadFile works.
6. How FastAPI calls predict_cnn().
7. How the Python dictionary becomes JSON.
8. How the frontend receives the response.
9. Why TensorFlow belongs in vision_engine rather than main.py.
10. Why FastAPI is acting as the API gateway.

Show the important code sections and explain them line-by-line where useful.

==================================================
SAFETY / PROJECT RULES
==================================================

Do NOT:

- redesign the whole project
- create duplicate engines folders
- create a second backend
- put CNN logic directly in main.py
- put FastAPI logic inside vision_engine
- modify the UI unnecessarily
- replace the existing frontend framework
- add a database
- add authentication
- add Docker
- add Redis
- add Celery
- add unnecessary dependencies
- invent model classes or preprocessing
- assume the class order without checking the trained model/training code

Make the smallest clean changes necessary.

At the end, provide:

1. Final modified file tree.
2. List of changed files.
3. Dependencies added.
4. Commands to install dependencies.
5. Command to start FastAPI.
6. How to test /docs.
7. How to test the frontend.
8. A short explanation of the complete request flow.

Do not modify files that are unrelated to this CNN → FastAPI → frontend integration.
 
