"""Ultralytics YOLO inference for plant disease detection.

The module is independent of FastAPI. It loads the repository's ``yolo.pt``
checkpoint once and exposes the plain ``predict_yolo(image_path)`` function.
"""

from __future__ import annotations

import atexit
import tempfile
import time
import zipfile
from pathlib import Path
from threading import Lock

from PIL import Image, UnidentifiedImageError
from ultralytics import YOLO


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "yolo.pt"

_model = None
_model_lock = Lock()
_packed_checkpoint: Path | None = None


def _cleanup_packed_checkpoint() -> None:
    if _packed_checkpoint and _packed_checkpoint.exists():
        _packed_checkpoint.unlink()


def _checkpoint_path() -> Path:
    """Return a loadable checkpoint path without modifying the source model."""
    global _packed_checkpoint

    if MODEL_PATH.is_file():
        return MODEL_PATH

    if not MODEL_PATH.is_dir():
        raise FileNotFoundError("YOLO model yolo.pt was not found in the project root.")

    # The supplied yolo.pt is an extracted PyTorch archive. Ultralytics expects
    # the same files in a .pt zip container, so rebuild that container in %TEMP%.
    archive_root = MODEL_PATH / "best"
    required_files = (
        archive_root / "data.pkl",
        archive_root / "version",
        archive_root / "byteorder",
    )
    if not all(path.is_file() for path in required_files):
        raise FileNotFoundError("The yolo.pt directory is not a valid PyTorch checkpoint.")

    if _packed_checkpoint and _packed_checkpoint.exists():
        return _packed_checkpoint

    temporary = tempfile.NamedTemporaryFile(
        prefix="plantai-yolo-",
        suffix=".pt",
        delete=False,
    )
    temporary_path = Path(temporary.name)
    temporary.close()

    with zipfile.ZipFile(temporary_path, mode="w", compression=zipfile.ZIP_STORED) as archive:
        for source in MODEL_PATH.rglob("*"):
            if source.is_file():
                archive.write(source, source.relative_to(MODEL_PATH).as_posix())

    _packed_checkpoint = temporary_path
    atexit.register(_cleanup_packed_checkpoint)
    return temporary_path


def _get_model():
    global _model

    if _model is None:
        with _model_lock:
            if _model is None:
                _model = YOLO(str(_checkpoint_path()))
    return _model


def _validate_image(image_path: Path) -> None:
    if not image_path.is_file():
        raise FileNotFoundError("Input image was not found.")

    try:
        with Image.open(image_path) as image:
            image.verify()
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError("Input file is not a readable image.") from exc


def _names_by_id(model) -> dict[int, str]:
    names = model.names
    if isinstance(names, dict):
        return {int(class_id): str(name) for class_id, name in names.items()}
    return {class_id: str(name) for class_id, name in enumerate(names)}


def _humanize(value: str) -> str:
    return value.replace("__", " ").replace("_", " ").strip().title()


def _format_class_name(raw_name: str) -> tuple[str, str]:
    if "___" in raw_name:
        plant_name, disease_name = raw_name.split("___", 1)
        return _humanize(plant_name), _humanize(disease_name)

    if "_" in raw_name:
        plant_name, disease_name = raw_name.split("_", 1)
        return _humanize(plant_name), _humanize(disease_name)

    return "Unknown", _humanize(raw_name)


def _percentage(value: float, total: float) -> float:
    if total <= 0:
        return 0.0
    return max(0.0, min(100.0, value / total * 100.0))


def predict_yolo(image_path: str) -> dict:
    """Run real Ultralytics YOLO inference on one image.

    The returned dictionary includes the frontend-compatible fields and the
    original pixel-coordinate bounding boxes for API consumers that need them.
    """
    source = Path(image_path)
    _validate_image(source)
    model = _get_model()
    names = _names_by_id(model)

    start = time.perf_counter()
    results = model.predict(source=str(source), verbose=False)
    inference_ms = int((time.perf_counter() - start) * 1000)

    result = results[0]
    boxes = result.boxes
    image_height, image_width = result.orig_shape
    detections = []

    if boxes is not None:
        for index in range(len(boxes)):
            class_id = int(boxes.cls[index].item())
            class_name = names.get(class_id, f"Class {class_id}")
            confidence = float(boxes.conf[index].item())
            x1, y1, x2, y2 = [float(value) for value in boxes.xyxy[index].tolist()]
            plant, disease = _format_class_name(class_name)
            status = "healthy" if "healthy" in class_name.lower() else "diseased"

            detections.append(
                {
                    "class_id": class_id,
                    "class_name": class_name,
                    "confidence": confidence,
                    "bbox": {
                        "x1": x1,
                        "y1": y1,
                        "x2": x2,
                        "y2": y2,
                    },
                    # These fields preserve the existing frontend overlay contract.
                    "label": disease,
                    "x": _percentage(x1, image_width),
                    "y": _percentage(y1, image_height),
                    "width": _percentage(max(0.0, x2 - x1), image_width),
                    "height": _percentage(max(0.0, y2 - y1), image_height),
                    "status": status,
                    "_plant": plant,
                    "_disease": disease,
                }
            )

    detections.sort(key=lambda detection: detection["confidence"], reverse=True)
    healthy_regions = sum(
        1 for detection in detections if detection["status"] == "healthy"
    )
    diseased_regions = len(detections) - healthy_regions

    if detections:
        top_detection = detections[0]
        plant = top_detection["_plant"]
        disease = (
            "Healthy"
            if top_detection["status"] == "healthy"
            else top_detection["_disease"]
        )
        confidence = top_detection["confidence"]
        severity = "Unknown"
    else:
        plant = "Unknown"
        disease = "No detections"
        confidence = 0.0
        severity = "None"

    for detection in detections:
        detection.pop("_plant", None)
        detection.pop("_disease", None)

    return {
        "plant": plant,
        "disease": disease,
        "confidence": confidence,
        "severity": severity,
        "objects_detected": len(detections),
        "healthy_regions": healthy_regions,
        "diseased_regions": diseased_regions,
        "detections": detections,
        "detection_count": len(detections),
        "inference_time_ms": inference_ms,
        "inferenceMs": inference_ms,
    }
