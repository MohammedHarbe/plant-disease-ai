#!/usr/bin/env python
"""Quick test script for CNN prediction."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Now import
from vision_engine.fake_cnn import predict_cnn

# Test - reuses the same sample image the YOLO test script uses.
print("=" * 60)
print("Testing CNN Model Directly")
print("=" * 60)

result = predict_cnn("_test_green.jpg")

print("\n[SUCCESS] CNN prediction returned:")
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
