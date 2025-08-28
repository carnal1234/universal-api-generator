# 🚀 Universal API Generator

A powerful tool for automatically analyzing and documenting REST APIs with a modern React frontend and Python backend.

## 📋 **Overview**

Universal API Generator is a comprehensive solution that combines:
- **Python Backend**: Intelligent API analysis and Swagger specification generation
- **React Frontend**: Modern, responsive UI with Swagger UI integration
- **Integrated Server**: Single command to run both frontend and backend

## 🏗️ **Architecture**

```
universal_api_generator/
├── universal_api_backend/     # Python backend
│   ├── app.py                # Flask server
│   ├── universal_api_generator.py  # Main API analyzer
│   ├── swagger_generator.py   # Swagger spec generator
│   ├── run_server.py         # Integrated server runner
│   └── requirements.txt      # Python dependencies
├── universal_api_frontend/    # React frontend
│   ├── src/                  # React source code
│   ├── public/               # Static assets
│   ├── package.json          # NPM configuration
│   └── tailwind.config.js    # Tailwind CSS config
└── README.md                 # This file
```

## 🚀 **Quick Start**

### **Option 1: Integrated Server (Recommended)**
```bash
# Clone the repository
git clone <your-repo-url>
cd universal_api_generator

# Run the integrated server
cd universal_api_backend
python3 run_server.py

# Open http://localhost:5000 in your browser
```

### **Option 2: Separate Frontend/Backend**
```bash
# Backend: Generate API documentation
cd universal_api_backend
python3 universal_api_generator.py https://api.example.com --swagger

# Frontend: Start React development server
cd universal_api_frontend
npm install
npm run dev
```

## 🔧 **Features**

### **Backend Features**
- ✅ **Intelligent Endpoint Discovery**: Automatic detection of API endpoints
- ✅ **Custom Endpoint Support**: Specify exact endpoints for targeted analysis
- ✅ **Parameter Analysis**: Comprehensive parameter type detection and validation
- ✅ **CRUD Operation Detection**: Automatic identification of Create, Read, Update, Delete operations
- ✅ **Swagger Generation**: Generate OpenAPI/Swagger specifications
- ✅ **Response Schema Analysis**: Infer data structures from API responses

### **Frontend Features**
- ✅ **Modern UI**: Clean, responsive design inspired by open-lovable
- ✅ **Swagger UI Integration**: Professional API documentation viewer
- ✅ **Custom Endpoints**: Specify exact endpoints for efficient analysis
- ✅ **Advanced Options**: API name, description, and custom endpoint configuration
- ✅ **Tailwind CSS**: Modern utility-first styling
- ✅ **Real-time Feedback**: Progress indicators and status updates

### **Integration Features**
- ✅ **Single Command**: Run both frontend and backend with one command
- ✅ **Auto-build**: Automatic frontend building and dependency installation
- ✅ **API Endpoints**: RESTful API for frontend-backend communication
- ✅ **Error Handling**: Graceful error handling and user feedback

## 📖 **Usage**

### **Command Line Usage**
```bash
# Basic analysis
python3 universal_api_backend/universal_api_generator.py https://api.example.com

# With custom endpoints
python3 universal_api_backend/universal_api_generator.py https://api.example.com -e /users /posts --swagger

# From endpoints file
python3 universal_api_backend/universal_api_generator.py https://api.example.com -f endpoints.txt --swagger
```

### **Web Interface Usage**
1. **Start Server**: Run `python3 run_server.py`
2. **Open Browser**: Navigate to `http://localhost:5000`
3. **Enter API URL**: Add your API URL and optional custom endpoints
4. **Generate Docs**: Click "Analyze API" to generate documentation
5. **View Results**: Swagger UI displays the generated documentation

## 🛠️ **Installation**

### **Prerequisites**
- Python 3.8+
- Node.js 16+
- npm or yarn

### **Backend Setup**
```bash
cd universal_api_backend
pip install -r requirements.txt
```

### **Frontend Setup**
```bash
cd universal_api_frontend
npm install
```

## 🔧 **Configuration**

### **Backend Configuration**
- **Timeout**: Adjust request timeout in `universal_api_generator.py`
- **Delay**: Configure delay between requests
- **Custom Endpoints**: Specify exact endpoints for targeted analysis

### **Frontend Configuration**
- **Styling**: Modify `tailwind.config.js` for theme customization
- **Components**: Update `src/styles.js` for component-specific styles
- **API Integration**: Configure API endpoints in `src/App.js`

## 📁 **Project Structure**

### **Backend (`universal_api_backend/`)**
- `app.py` - Flask server with API endpoints
- `universal_api_generator.py` - Main API analysis engine
- `swagger_generator.py` - Swagger specification generator
- `run_server.py` - Integrated server runner
- `build_frontend.py` - Frontend build automation
- `requirements.txt` - Python dependencies

### **Frontend (`universal_api_frontend/`)**
- `src/App.js` - Main React component
- `src/index.js` - Application entry point
- `src/styles.js` - Tailwind CSS component styles
- `src/index.css` - Global styles and Tailwind directives
- `package.json` - NPM configuration and scripts
- `tailwind.config.js` - Tailwind CSS configuration

## 🚀 **Deployment**

### **Development**
```bash
# Integrated mode
cd universal_api_backend
python3 run_server.py

# Separate mode
cd universal_api_frontend && npm run dev  # Frontend
cd universal_api_backend && python3 app.py  # Backend
```

### **Production**
```bash
# Build frontend
cd universal_api_frontend
npm run build

# Run production server
cd universal_api_backend
python3 app.py
```

## 🛠️ **Troubleshooting**

### **Common Issues**
- **404 Errors**: Build frontend manually with `python3 build_frontend.py`
- **npm Not Found**: Install Node.js from https://nodejs.org/
- **Port Conflicts**: Use different port with `FLASK_PORT=5001 python3 app.py`
- **Dependencies**: Install with `pip install -r requirements.txt`

### **Debug Mode**
```bash
# Enable debug logging
cd universal_api_backend
FLASK_DEBUG=1 python3 app.py
```

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 **Acknowledgments**

- **open-lovable**: UI design inspiration
- **Swagger UI**: API documentation viewer
- **Tailwind CSS**: Utility-first CSS framework
- **Flask**: Python web framework
- **React**: Frontend framework

## 📞 **Support**

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the documentation in each directory

---

**Made with ❤️ for the developer community**
