#!/usr/bin/env python3
"""
Frontend Builder for Universal API Generator

This script builds the React frontend for the Universal API Generator.
"""

import subprocess
import sys
from pathlib import Path

def main():
    # Get the frontend directory
    frontend_dir = Path(__file__).parent.parent / "universal_api_frontend"
    
    print("🔨 Building React Frontend")
    print("=" * 30)
    print(f"📁 Frontend directory: {frontend_dir}")
    
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return 1
    
    # Check if package.json exists
    package_json = frontend_dir / "package.json"
    if not package_json.exists():
        print("❌ package.json not found!")
        return 1
    
    try:
        # Install dependencies
        print("\n📥 Installing dependencies...")
        subprocess.run(['npm', 'install'], cwd=frontend_dir, check=True)
        print("✅ Dependencies installed")
        
        # Build the app
        print("\n🔨 Building React app...")
        subprocess.run(['npm', 'run', 'build'], cwd=frontend_dir, check=True)
        print("✅ Frontend built successfully!")
        
        # Check if build directory was created
        build_dir = frontend_dir / "build"
        if build_dir.exists():
            print(f"📁 Build directory: {build_dir}")
            print("🎉 Frontend is ready to serve!")
        else:
            print("❌ Build directory was not created")
            return 1
        
        return 0
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return 1
    except FileNotFoundError:
        print("❌ npm not found. Please install Node.js and npm first.")
        print("   Download from: https://nodejs.org/")
        return 1

if __name__ == "__main__":
    sys.exit(main())
