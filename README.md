# Universal API Generator

A comprehensive tool for automatically discovering, analyzing, and documenting REST APIs with a modern React frontend and Python backend.

## 🚀 **Quick Start**

### **Option 1: Integrated Server (Recommended)**
```bash
# Run the integrated server (serves both frontend and backend)
cd universal_api_backend
python3 run_server.py

# Then open http://localhost:5000 in your browser
```

### **Option 2: Manual Frontend Build**
```bash
# If you encounter 404 errors for JS/CSS files, build the frontend manually:
cd universal_api_backend
python3 build_frontend.py

# Then run the server
python3 run_server.py
```

### **Option 3: Separate Frontend/Backend**
```bash
# Backend: Generate API documentation
cd universal_api_backend
python3 universal_api_generator.py https://api.example.com --swagger

# Frontend: Start React development server
cd universal_api_frontend
npm run dev
```

### **Option 4: Test the Integration**
```bash
# Start the server
cd universal_api_backend
python3 run_server.py

# In another terminal, test the API
cd universal_api_backend
python3 test_integration.py
```

## 📁 **Project Structure**

```
universal_api_generator/
├── universal_api_backend/     # Python backend
│   ├── universal_api_generator.py  # Main API generator
│   ├── app.py                 # Flask server (integrated mode)
│   ├── run_server.py          # Server runner script
│   ├── test_integration.py    # Integration tests
│   ├── swagger_generator.py   # Swagger spec generator
│   └── requirements.txt       # Python dependencies
├── universal_api_frontend/    # React frontend
│   ├── src/                   # React source code
│   ├── public/                # Static assets
│   └── package.json           # Node.js dependencies
└── README.md                  # This file
```

## 🎯 **Features**

### **Frontend (React + Tailwind CSS)**
- ✅ **Modern UI**: Clean, responsive design inspired by open-lovable
- ✅ **Advanced Options**: Custom endpoints, API name, and description
- ✅ **Real-time Integration**: Direct API calls to backend
- ✅ **File Upload**: Upload existing swagger.json files
- ✅ **Example Presets**: Pre-configured API examples

### **Backend (Python)**
- ✅ **Universal Discovery**: Automatically finds API endpoints
- ✅ **Custom Endpoints**: Specify exact endpoints for efficiency
- ✅ **Conservative Validation**: Only accepts 200 status codes
- ✅ **Core HTTP Methods**: Tests GET, POST, and DELETE
- ✅ **Swagger Generation**: Creates OpenAPI 3.0 specifications

### **Integrated Server**
- ✅ **Single Command**: Run both frontend and backend together
- ✅ **API Endpoints**: RESTful API for generating documentation
- ✅ **Auto-build**: Automatically builds React frontend
- ✅ **CORS Support**: Handles cross-origin requests

## 🔧 **Usage**

### **Integrated Mode (Recommended)**
1. **Start Server**: `cd universal_api_backend && python3 run_server.py`
2. **Open Browser**: Navigate to `http://localhost:5000`
3. **Enter API URL**: Add your API URL and optional custom endpoints
4. **Generate Docs**: Click "Analyze API" to generate documentation
5. **View Results**: Swagger UI displays the generated documentation

### **Command Line Mode**
```bash
# Basic analysis
python3 universal_api_backend/universal_api_generator.py https://api.example.com

# With custom endpoints
python3 universal_api_backend/universal_api_generator.py https://api.example.com -e /users /posts --swagger

# From endpoints file
python3 universal_api_backend/universal_api_generator.py https://api.example.com -f endpoints.txt --swagger
```

## 🛠️ **Troubleshooting**

### **404 Errors for JS/CSS Files** ✅ **FIXED**
The 404 errors for JavaScript and CSS files have been resolved. The Flask server now properly serves static files from the React build directory.

If you still encounter issues:

```bash
# Build the frontend manually
cd universal_api_backend
python3 build_frontend.py

# Then run the server
python3 run_server.py
```

### **npm Not Found**
If you get "npm not found" errors:

1. **Install Node.js**: Download from https://nodejs.org/
2. **Verify Installation**: Run `npm --version`
3. **Rebuild Frontend**: Run `python3 build_frontend.py`

### **Port Already in Use**
If port 5000 is already in use:

```bash
# Kill existing process
lsof -ti:5000 | xargs kill -9

# Or use a different port
cd universal_api_backend
FLASK_PORT=5001 python3 app.py
```

### **Python Dependencies Missing**
If you get import errors:

```bash
cd universal_api_backend
pip install -r requirements.txt
```

## 📋 **API Endpoints**

### **POST /api/generate**
Generate API documentation from a URL.

**Request Body:**
```json
{
  "url": "https://api.example.com",
  "customEndpoints": "/users\n/posts\n/comments",
  "apiName": "My Awesome API",
  "apiDescription": "A comprehensive API for managing data"
}
```

**Response:**
```json
{
  "success": true,
  "swagger": { /* OpenAPI 3.0 specification */ },
  "message": "API documentation generated successfully"
}
```

### **GET /api/health**
Health check endpoint.

## 🛠️ **Development**

### **Frontend Development**
```bash
cd universal_api_frontend
npm install
npm run dev
```

### **Backend Development**
```bash
cd universal_api_backend
pip install -r requirements.txt
python3 universal_api_generator.py --help
```

### **Building for Production**
```bash
# Build frontend
cd universal_api_frontend
npm run build

# Run integrated server
python3 run_server.py
```

## 📝 **Configuration**

### **Environment Variables**
- `FLASK_ENV`: Set to `development` for debug mode
- `FLASK_PORT`: Port for the Flask server (default: 5000)

### **Customization**
- **Frontend**: Modify `universal_api_frontend/src/App.js` and `styles.js`
- **Backend**: Customize `universal_api_backend/universal_api_generator.py`
- **API**: Extend `universal_api_backend/app.py` for additional endpoints

## 🎨 **UI Features**

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Tailwind CSS**: Modern utility-first styling
- **Progress Indicators**: Real-time feedback during analysis
- **Error Handling**: Clear error messages and recovery options
- **File Upload**: Drag-and-drop swagger.json upload
- **Example APIs**: Quick access to popular API examples

## 🔍 **Supported APIs**

The tool works with most REST APIs including:
- **JSON APIs**: Standard JSON REST APIs
- **OpenAPI/Swagger**: APIs with OpenAPI specifications
- **Documentation**: APIs with HTML documentation pages
- **Custom Endpoints**: Any API where you know the endpoints

## 📚 **Documentation**

- [Backend Documentation](universal_api_backend/README.md)
- [Frontend Documentation](universal_api_frontend/README.md)
- [API Reference](universal_api_backend/README.md#api-endpoints)

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 **License**

MIT License - see LICENSE file for details.
