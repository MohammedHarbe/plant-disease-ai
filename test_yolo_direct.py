#!/usr/bin/env python
"""Quick test script for YOLO prediction."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Now import
from vision_engine.fake_yolo import predict_yolo

# Test
print("=" * 60)
print("Testing YOLO Fake Model Directly")
print("=" * 60)

result = predict_yolo("test_image.jpg")

print("\n[SUCCESS] YOLO prediction returned:")
print()
for key, value in result.items():
    if isinstance(value, (list, dict)):
        print(f"  {key}:")
        print(f"    {value}")
    else:
        print(f"  {key}: {value}")

print("\n" + "=" * 60)
print("Test Complete!")
print("=" * 60)
