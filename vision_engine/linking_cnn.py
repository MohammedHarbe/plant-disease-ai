"""
CNN inference for plant disease classification.

ARCHITECTURE:
- This module is independent of FastAPI - it exposes a single plain
  Python function, predict_cnn(), that backend/main.py imports and calls.
- No FastAPI / web code lives in this file.

MODEL DETAILS (found by loading best_model.keras directly and inspecting it,
NOT guessed):
- Backbone: EfficientNetB0 (transfer learning), Dense(15, softmax) head.
- model.input_shape  == (None, 224, 224, 3)
- model.output_shape == (None, 15)
- The model's own `efficientnetb0` sub-model contains its own internal
  Rescaling + Normalization layers. That means this file must feed it RAW
  pixel values in [0, 255] as float32 - do NOT divide by 255 here, or the
  image will be normalized twice and predictions will be wrong.
- The model also contains a `data_augmentation` block (RandomFlip/
  RandomRotation/RandomZoom/RandomContrast). Keras automatically disables
  these layers during inference (model.predict runs with training=False),
  so nothing needs to be done about them here.
- The final Dense layer already has activation="softmax", so model.predict()
  output is already a probability distribution over the 15 classes.

CLASS NAMES - CONFIRMED from plant-disease-detection-using-imagenet50.ipynb:
Dataset is Kaggle's emmarex/plantdisease (PlantVillage), split with
tf.keras.utils.image_dataset_from_directory (which sorts class folders
alphabetically and exposes that order as `.class_names`). The notebook's
own saved cell output printed `train_ds.class_names` with its index -
that exact printed list is CLASS_NAMES below, index-for-index. This is no
longer a guess.
"""

import time
from pathlib import Path

import numpy as np
import keras
from PIL import Image, UnidentifiedImageError

# ---------------------------------------------------------------------------
# Class names, in the exact order train_ds.class_names printed during
# training (see module docstring) - index position == model output index.
# ---------------------------------------------------------------------------
CLASS_NAMES = [
    "Pepper__bell___Bacterial_spot",
    "Pepper__bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Tomato_Bacterial_spot",
    "Tomato_Early_blight",
    "Tomato_Late_blight",
    "Tomato_Leaf_Mold",
    "Tomato_Septoria_leaf_spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite",
    "Tomato__Target_Spot",
    "Tomato__Tomato_YellowLeaf__Curl_Virus",
    "Tomato__Tomato_mosaic_virus",
    "Tomato_healthy",
]

# From model.input_shape: (None, 224, 224, 3)
IMG_SIZE = (224, 224)

# vision_engine/linking_cnn.py -> parent (vision_engine/) -> parent (project root)
_MODEL_PATH = Path(__file__).resolve().parent.parent / "best_model.keras"

# Module-level cache so the (large) model is loaded from disk only once,
# the first time predict_cnn() is actually called - not on every request.
_model = None


def _get_model():
    global _model
    if _model is None:
        if not _MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Model file not found at expected path: {_MODEL_PATH.name} "
                f"(looked in project root)."
            )
        _model = keras.models.load_model(_MODEL_PATH)
    return _model


def _format_label(raw_label: str) -> tuple[str, str]:
    """
    Convert a raw training-folder-style label such as
    'Potato___Early_blight' or 'Pepper__bell___Bacterial_spot' into a
    human-readable (plant, disease) pair for the API response.
    """
    if "___" in raw_label:
        plant_part, disease_part = raw_label.split("___", 1)
    else:
        plant_part, _, disease_part = raw_label.partition("_")

    plant = plant_part.replace("__", " ").replace("_", " ").strip().title()
    disease_part = disease_part.replace("__", " ").replace("_", " ").strip()
    disease = disease_part.title() if disease_part else "Unknown"
    return plant, disease


def predict_cnn(image_path: str) -> dict:
    """
    Run real CNN inference on an image and return a result shaped to match
    the frontend's CnnResult type (frontend/.../src/types/index.ts):

        {
            "plant": str,
            "disease": str,
            "confidence": float,
            "predictions": [{"label": str, "confidence": float}, ...],
            "imageUrl": str,
            "inferenceMs": int,
        }

    Args:
        image_path: Path to an image file already saved on disk.

    Raises:
        FileNotFoundError: if best_model.keras is missing.
        ValueError: if the file at image_path is not a readable image.
    """
    model = _get_model()

    try:
        img = Image.open(image_path).convert("RGB").resize(IMG_SIZE)
    except UnidentifiedImageError as exc:
        raise ValueError("Could not read the uploaded file as an image.") from exc

    # Raw [0, 255] float32 pixels - the model normalizes internally (see
    # module docstring). Do not divide by 255 here.
    arr = np.asarray(img, dtype=np.float32)
    batch = np.expand_dims(arr, axis=0)

    start = time.perf_counter()
    probs = model.predict(batch, verbose=0)[0]
    inference_ms = int((time.perf_counter() - start) * 1000)

    top_k = min(3, len(probs))
    top_indices = np.argsort(probs)[::-1][:top_k]

    predictions = []
    for idx in top_indices:
        idx = int(idx)
        raw_label = CLASS_NAMES[idx] if idx < len(CLASS_NAMES) else f"Class_{idx}"
        _, disease_label = _format_label(raw_label)
        predictions.append({"label": disease_label, "confidence": float(probs[idx])})

    top_idx = int(top_indices[0])
    top_raw = CLASS_NAMES[top_idx] if top_idx < len(CLASS_NAMES) else f"Class_{top_idx}"
    plant, disease = _format_label(top_raw)

    return {
        "plant": plant,
        "disease": disease,
        "confidence": float(probs[top_idx]),
        "predictions": predictions,
        "imageUrl": "",
        "inferenceMs": inference_ms,
    }
