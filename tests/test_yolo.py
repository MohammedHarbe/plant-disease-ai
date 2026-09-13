from pathlib import Path

from vision_engine.linking_yolo import predict_yolo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEST_IMAGE = PROJECT_ROOT / "test" / "_test_green.jpg"


def test_predict_yolo_uses_local_model_and_returns_serializable_result():
    result = predict_yolo(str(TEST_IMAGE))

    assert result["detection_count"] == len(result["detections"])
    assert result["image_width"] > 0
    assert result["image_height"] > 0
    assert result["inference_time_ms"] >= 0
    assert result["inferenceMs"] == result["inference_time_ms"]
    assert isinstance(result["detections"], list)

    for detection in result["detections"]:
        assert isinstance(detection["class_id"], int)
        assert isinstance(detection["class_name"], str)
        assert 0.0 <= detection["confidence"] <= 1.0
        assert set(detection["bbox"]) == {"x1", "y1", "x2", "y2"}
        assert detection["bbox"]["x1"] <= detection["bbox"]["x2"]
        assert detection["bbox"]["y1"] <= detection["bbox"]["y2"]


def test_predict_yolo_rejects_missing_image():
    missing_image = PROJECT_ROOT / "test" / "does-not-exist.jpg"

    try:
        predict_yolo(str(missing_image))
    except FileNotFoundError:
        pass
    else:
        raise AssertionError("predict_yolo should reject a missing image")
