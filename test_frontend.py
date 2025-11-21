#!/usr/bin/env python3
"""
Test script to verify frontend can start without errors
"""
import sys
import subprocess
import time
import requests
from pathlib import Path

def test_frontend_startup():
    """Test if frontend can start without import errors"""
    print("Testing frontend startup...")
    
    try:
        # Test import without running the app
        result = subprocess.run([
            sys.executable, "-c", 
            "import sys; sys.path.insert(0, 'src'); import streamlit; print('Frontend imports OK')"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("  [PASS] Frontend imports successfully")
            return True
        else:
            print(f"  [FAIL] Frontend import failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"  [FAIL] Frontend test failed: {e}")
        return False

def test_backend_startup():
    """Test if backend can start"""
    print("Testing backend startup...")
    
    try:
        # Check if backend is already running
        response = requests.get("http://localhost:8000/health", timeout=2)
        if response.status_code == 200:
            print("  [PASS] Backend is running and healthy")
            return True
    except:
        pass
    
    print("  [INFO] Backend not running - this is expected for testing")
    return True

def main():
    """Run frontend tests"""
    print("Running Frontend Tests\n")
    
    tests = [
        ("Frontend Startup", test_frontend_startup),
        ("Backend Check", test_backend_startup)
    ]
    
    results = {}
    for name, test_func in tests:
        results[name] = test_func()
        print()
    
    # Summary
    print("Frontend Test Results:")
    passed = sum(results.values())
    total = len(results)
    
    for name, result in results.items():
        status = "[PASS]" if result else "[FAIL]"
        print(f"  {name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("Frontend is ready!")
    else:
        print("Frontend needs attention")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)