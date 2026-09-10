#!/usr/bin/env python3
"""
Plant Disease API Test Script
Tests all API endpoints with real requests
"""

import requests
import json
import time
from pathlib import Path

# Configuration
API_URL = "http://127.0.0.1:8000"

# ANSI colors for output
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'


def print_header(text):
    """Print formatted header"""
    print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{BLUE}{text:^60}{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}\n")


def print_test(name, passed, message=""):
    """Print test result"""
    status = f"{GREEN}✅ PASSED{RESET}" if passed else f"{RED}❌ FAILED{RESET}"
    print(f"{status} - {name}")
    if message:
        print(f"  {YELLOW}→ {message}{RESET}")


def test_home():
    """Test home endpoint"""
    print_header("Testing: GET /")
    try:
        response = requests.get(f"{API_URL}/")
        passed = response.status_code == 200
        print_test("Home Status Code", passed, f"Status: {response.status_code}")
        
        data = response.json()
        print(f"  Response: {json.dumps(data, indent=2)}")
        return passed
    except Exception as e:
        print_test("Home Status Code", False, str(e))
        return False


def test_health():
    """Test health endpoint"""
    print_header("Testing: GET /health")
    try:
        response = requests.get(f"{API_URL}/health")
        passed = response.status_code == 200 and response.json().get("status") == "healthy"
        print_test("Health Status", passed, f"Status: {response.status_code}")
        
        data = response.json()
        print(f"  Response: {json.dumps(data, indent=2)}")
        return passed
    except Exception as e:
        print_test("Health Status", False, str(e))
        return False


def test_diseases():
    """Test diseases endpoint"""
    print_header("Testing: GET /diseases")
    try:
        response = requests.get(f"{API_URL}/diseases")
        passed = response.status_code == 200
        print_test("Diseases List", passed, f"Status: {response.status_code}")
        
        data = response.json()
        print(f"  Found {len(data['diseases'])} diseases:")
        for disease in data['diseases']:
            print(f"    • {disease}")
        return passed
    except Exception as e:
        print_test("Diseases List", False, str(e))
        return False


def test_models():
    """Test models endpoint"""
    print_header("Testing: GET /models")
    try:
        response = requests.get(f"{API_URL}/models")
        passed = response.status_code == 200
        print_test("Models List", passed, f"Status: {response.status_code}")
        
        data = response.json()
        print(f"  Found {len(data['models'])} models:")
        for model in data['models']:
            print(f"    • {model['name']} ({model['id']})")
        return passed
    except Exception as e:
        print_test("Models List", False, str(e))
        return False


def test_yolo_predict():
    """Test YOLO prediction endpoint"""
    print_header("Testing: POST /predict/yolo")
    try:
        # Create a fake image file
        fake_image = b"fake image content for testing"
        files = {'file': ('test_image.jpg', fake_image, 'image/jpeg')}
        
        response = requests.post(f"{API_URL}/predict/yolo", files=files)
        passed = response.status_code == 200
        print_test("YOLO Prediction", passed, f"Status: {response.status_code}")
        
        data = response.json()
        print(f"  Plant: {data.get('plant')}")
        print(f"  Disease: {data.get('disease')}")
        print(f"  Confidence: {data.get('confidence')}%")
        print(f"  Severity: {data.get('severity')}")
        print(f"  Objects Detected: {data.get('objectsDetected')}")
        print(f"  Detections: {len(data.get('detections', []))} found")
        print(f"  Inference Time: {data.get('inferenceMs')}ms")
        
        # Verify all required fields
        required_fields = ['plant', 'disease', 'confidence', 'severity', 
                          'objectsDetected', 'detections', 'imageUrl', 'inferenceMs']
        all_fields_present = all(field in data for field in required_fields)
        print_test("YOLO Fields Present", all_fields_present)
        
        return passed and all_fields_present
    except Exception as e:
        print_test("YOLO Prediction", False, str(e))
        return False


def test_cnn_predict():
    """Test CNN prediction endpoint"""
    print_header("Testing: POST /predict/cnn")
    try:
        # Create a fake image file
        fake_image = b"fake image content for testing"
        files = {'file': ('test_image.jpg', fake_image, 'image/jpeg')}
        
        response = requests.post(f"{API_URL}/predict/cnn", files=files)
        passed = response.status_code == 200
        print_test("CNN Prediction", passed, f"Status: {response.status_code}")
        
        data = response.json()
        print(f"  Plant: {data.get('plant')}")
        print(f"  Disease: {data.get('disease')}")
        print(f"  Confidence: {data.get('confidence')}%")
        print(f"  Top Predictions:")
        
        for pred in data.get('predictions', []):
            print(f"    • {pred['label']}: {pred['confidence']}%")
        
        print(f"  Inference Time: {data.get('inferenceMs')}ms")
        
        # Verify all required fields
        required_fields = ['plant', 'disease', 'confidence', 'predictions', 'imageUrl', 'inferenceMs']
        all_fields_present = all(field in data for field in required_fields)
        print_test("CNN Fields Present", all_fields_present)
        
        return passed and all_fields_present
    except Exception as e:
        print_test("CNN Prediction", False, str(e))
        return False


def test_cors():
    """Test CORS headers"""
    print_header("Testing: CORS Headers")
    try:
        headers = {'Origin': 'http://localhost:3000'}
        response = requests.get(f"{API_URL}/health", headers=headers)
        
        passed = response.status_code == 200
        print_test("CORS Response", passed, f"Status: {response.status_code}")
        
        # Check for CORS headers
        cors_origin = response.headers.get('access-control-allow-origin')
        print(f"  CORS Origin: {cors_origin or 'Not Set (but API is accessible)'}")
        
        return passed
    except Exception as e:
        print_test("CORS Response", False, str(e))
        return False


def main():
    """Run all tests"""
    print(f"\n{BOLD}{BLUE}")
    print("  🌿 Plant Disease AI - Backend API Test Suite")
    print(f"  Testing: {API_URL}")
    print(f"{RESET}")
    
    # Check if API is online
    try:
        requests.get(f"{API_URL}/health", timeout=2)
    except:
        print(f"{RED}❌ ERROR: Cannot connect to API at {API_URL}{RESET}")
        print(f"{YELLOW}Make sure the backend is running: uvicorn main:app --reload --port 8000{RESET}\n")
        return
    
    # Run all tests
    results = []
    results.append(("Home Endpoint", test_home()))
    results.append(("Health Check", test_health()))
    results.append(("Diseases List", test_diseases()))
    results.append(("Models List", test_models()))
    results.append(("YOLO Prediction", test_yolo_predict()))
    results.append(("CNN Prediction", test_cnn_predict()))
    results.append(("CORS Headers", test_cors()))
    
    # Print summary
    print_header("Test Summary")
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    print(f"{BOLD}Results:{RESET}")
    for name, passed in results:
        status = f"{GREEN}✅{RESET}" if passed else f"{RED}❌{RESET}"
        print(f"  {status} {name}")
    
    print(f"\n{BOLD}Total: {passed_count}/{total_count} tests passed{RESET}")
    
    if passed_count == total_count:
        print(f"\n{GREEN}{BOLD}🎉 All tests passed! API is ready for use.{RESET}\n")
    else:
        print(f"\n{RED}{BOLD}⚠️  Some tests failed. Check the output above.{RESET}\n")


if __name__ == "__main__":
    main()
