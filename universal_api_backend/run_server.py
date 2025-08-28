#!/usr/bin/env python3
"""
Integrated Server Runner for Universal API Generator

This script runs the Flask server that serves both the frontend and backend API.
"""

import sys
import subprocess
import os
from pathlib import Path

def check_frontend_dependencies():
    """Check if frontend dependencies are available"""
    frontend_dir = Path(__file__).parent.parent / "universal_api_frontend"
    
    # Check if Node.js and npm are available
    try:
        subprocess.run(['npm', '--version'], capture_output=True, check=True)
        print("✅ npm is available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ npm not found. Please install Node.js and npm first.")
        print("   Download from: https://nodejs.org/")
        return False
    
    # Check if frontend directory exists
    if not frontend_dir.exists():
        print(f"❌ Frontend directory not found: {frontend_dir}")
        return False
    
    # Check if package.json exists
    package_json = frontend_dir / "package.json"
    if not package_json.exists():
        print(f"❌ package.json not found in frontend directory")
        return False
    
    print("✅ Frontend dependencies check passed")
    return True

def build_frontend():
    """Build the React frontend"""
    frontend_dir = Path(__file__).parent.parent / "universal_api_frontend"
    build_dir = frontend_dir / "build"
    
    if build_dir.exists():
        print("✅ Frontend already built")
        return True
    
    print("📦 Building frontend...")
    
    try:
        # Install dependencies if needed
        if not (frontend_dir / "node_modules").exists():
            print("📥 Installing frontend dependencies...")
            subprocess.run(['npm', 'install'], cwd=frontend_dir, check=True)
            print("✅ Dependencies installed")
        
        # Build the frontend
        print("🔨 Building React app...")
        subprocess.run(['npm', 'run', 'build'], cwd=frontend_dir, check=True)
        print("✅ Frontend built successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to build frontend: {e}")
        print("💡 You can still run the server - it will show instructions for manual build")
        return False

def main():
    # Get the current directory (backend)
    backend_dir = Path(__file__).parent.absolute()
    frontend_dir = backend_dir.parent / "universal_api_frontend"
    
    print("🚀 Universal API Generator - Server Runner")
    print("=" * 50)
    print(f"📁 Backend directory: {backend_dir}")
    print(f"📁 Frontend directory: {frontend_dir}")
    print()
    
    # Check if frontend directory exists
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        print(f"Expected: {frontend_dir}")
        return 1
    
    # Check frontend dependencies
    if not check_frontend_dependencies():
        print("\n💡 You can still run the server - it will show instructions for manual build")
    
    # Try to build frontend
    build_frontend()
    
    # Install backend dependencies
    print("\n📦 Installing backend dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      cwd=backend_dir, check=True)
        print("✅ Backend dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install backend dependencies: {e}")
        return 1
    
    # Run the Flask server
    print("\n🚀 Starting integrated server...")
    print("🌐 Server will be available at: http://localhost:5000")
    print("📋 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "app.py"], cwd=backend_dir, check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
