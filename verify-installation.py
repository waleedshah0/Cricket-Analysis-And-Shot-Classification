#!/usr/bin/env python3
"""
Verification script to check if all required dependencies are installed correctly
"""

import sys
import importlib

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9 or higher is required")
        return False
    else:
        print("✅ Python version is compatible")
        return True

def check_package(package_name, min_version=None):
    """Check if a package is installed"""
    try:
        package = importlib.import_module(package_name)
        if hasattr(package, '__version__'):
            version = package.__version__
            status = "✅"
            if min_version:
                # Simple version comparison (works for most cases)
                version_parts = [int(x) for x in version.split('.')[:2]]
                min_version_parts = [int(x) for x in min_version.split('.')[:2]]
                if version_parts < min_version_parts:
                    status = "⚠️"
            print(f"{status} {package_name} ({version})")
        else:
            print(f"✅ {package_name} (version unknown)")
        return True
    except ImportError:
        print(f"❌ {package_name} is not installed")
        return False

def main():
    print("Verifying Cricket AI Squad Installation...\n")
    
    # Check Python version
    python_ok = check_python_version()
    print()
    
    # Check required packages
    required_packages = [
        ("fastapi", "0.68.0"),
        ("uvicorn", "0.15.0"),
        ("tensorflow", "2.12.0"),
        ("cv2", None),  # OpenCV
        ("numpy", "1.23.5"),
        ("requests", "2.31.0")
    ]
    
    all_packages_ok = True
    for package, min_version in required_packages:
        if not check_package(package, min_version):
            all_packages_ok = False
    
    print()
    
    # Check for model weights file
    import os
    model_path = "model_weights.h5"
    if os.path.exists(model_path):
        size = os.path.getsize(model_path)
        print(f"✅ Model weights file found ({size / (1024*1024):.1f} MB)")
    else:
        print(f"⚠️ Model weights file '{model_path}' not found")
        print("   You need to obtain this file for the application to work")
    
    print()
    
    # Final status
    if python_ok and all_packages_ok:
        print("🎉 All checks passed! You're ready to run the application.")
        print("   Run 'python api.py' to start the backend server.")
    else:
        print("⚠️ Some issues detected. Please check the output above.")
        print("   Refer to TROUBLESHOOTING.md for detailed solutions.")

if __name__ == "__main__":
    main()