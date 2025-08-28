from flask import Flask, request, jsonify, send_from_directory, render_template_string
from flask_cors import CORS
import subprocess
import json
import os
import sys
from pathlib import Path

# Get the current directory (backend)
BACKEND_DIR = Path(__file__).parent.absolute()
FRONTEND_DIR = BACKEND_DIR.parent / "universal_api_frontend"
BUILD_DIR = FRONTEND_DIR / "build"

# Create Flask app with static folder configuration
app = Flask(__name__, 
           static_folder=str(BUILD_DIR),
           static_url_path='')
CORS(app)  # Enable CORS for all routes

def ensure_frontend_built():
    """Ensure the React frontend is built"""
    if not BUILD_DIR.exists():
        print("React build not found. Building frontend...")
        try:
            # Check if npm is available
            subprocess.run(['npm', '--version'], cwd=FRONTEND_DIR, check=True, capture_output=True)
            
            # Install dependencies if needed
            if not (FRONTEND_DIR / "node_modules").exists():
                print("Installing frontend dependencies...")
                subprocess.run(['npm', 'install'], cwd=FRONTEND_DIR, check=True)
            
            # Build the frontend
            subprocess.run(['npm', 'run', 'build'], cwd=FRONTEND_DIR, check=True)
            print("Frontend built successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to build frontend: {e}")
            return False
        except FileNotFoundError:
            print("npm not found. Please install Node.js and npm first")
            return False
    return True

@app.route('/')
def serve_frontend():
    """Serve the React frontend"""
    if not BUILD_DIR.exists():
        return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Universal API Generator</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                .error { color: #d32f2f; background: #ffebee; padding: 20px; border-radius: 8px; margin: 20px; }
                .info { color: #1976d2; background: #e3f2fd; padding: 20px; border-radius: 8px; margin: 20px; }
                code { background: #f5f5f5; padding: 2px 6px; border-radius: 4px; }
            </style>
        </head>
        <body>
            <h1>🚀 Universal API Generator</h1>
            <div class="error">
                <h2>Frontend Not Built</h2>
                <p>The React frontend has not been built yet.</p>
            </div>
            <div class="info">
                <h3>To fix this:</h3>
                <ol style="text-align: left; display: inline-block;">
                    <li>Make sure Node.js and npm are installed</li>
                    <li>Run: <code>cd universal_api_frontend && npm install</code></li>
                    <li>Run: <code>cd universal_api_frontend && npm run build</code></li>
                    <li>Restart the server</li>
                </ol>
            </div>
            <div class="info">
                <h3>Or use the API directly:</h3>
                <p>You can still use the API endpoints:</p>
                <ul style="text-align: left; display: inline-block;">
                    <li><code>POST /api/generate</code> - Generate API documentation</li>
                    <li><code>GET /api/health</code> - Health check</li>
                </ul>
            </div>
        </body>
        </html>
        ''')
    
    return send_from_directory(BUILD_DIR, "index.html")

@app.route('/api/generate', methods=['POST'])
def generate_api_docs():
    """API endpoint to generate API documentation"""
    try:
        data = request.get_json()
        url = data.get('url')
        custom_endpoints = data.get('customEndpoints', '')
        api_name = data.get('apiName', '')
        api_description = data.get('apiDescription', '')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Build the command
        cmd = [sys.executable, 'universal_api_generator.py', url, '--swagger']
        
        # Add custom endpoints if provided
        if custom_endpoints.strip():
            endpoints = [ep.strip() for ep in custom_endpoints.split('\n') if ep.strip() and not ep.startswith('#')]
            if endpoints:
                cmd.extend(['-e'] + endpoints)
        
        print(f"Running command: {' '.join(cmd)}")
        
        # Run the universal API generator
        result = subprocess.run(
            cmd,
            cwd=BACKEND_DIR,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode != 0:
            error_msg = result.stderr or result.stdout
            print(f"Error running generator: {error_msg}")
            return jsonify({
                'error': 'Failed to generate API documentation',
                'details': error_msg
            }), 500
        
        # Check if swagger.json was generated
        swagger_file = BACKEND_DIR / "swagger.json"
        if not swagger_file.exists():
            return jsonify({
                'error': 'Swagger file was not generated',
                'details': result.stdout
            }), 500
        
        # Read and return the swagger.json content
        with open(swagger_file, 'r', encoding='utf-8') as f:
            swagger_content = json.load(f)
        
        # Add metadata
        swagger_content['info']['title'] = api_name or f"API Documentation for {url}"
        if api_description:
            swagger_content['info']['description'] = api_description
        
        return jsonify({
            'success': True,
            'swagger': swagger_content,
            'message': 'API documentation generated successfully'
        })
        
    except subprocess.TimeoutExpired:
        return jsonify({
            'error': 'Generation timed out (took longer than 5 minutes)'
        }), 408
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({
            'error': 'An unexpected error occurred',
            'details': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'API server is running'})

if __name__ == '__main__':
    # Ensure frontend is built
    ensure_frontend_built()
    
    print("Starting Flask server...")
    print(f"Backend directory: {BACKEND_DIR}")
    print(f"Frontend directory: {FRONTEND_DIR}")
    app.run(debug=True, host='0.0.0.0', port=5000)
