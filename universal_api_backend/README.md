# Universal API Generator - Backend

This folder contains the Python backend for the Universal API Generator.

## 📁 **Files**

### **Core Generators**
- `universal_api_generator.py` - Main universal API generator with advanced features
- `simple_api_generator.py` - Simple API generator for basic CRUD operations
- `swagger_generator.py` - Converts analysis.json to OpenAPI 3.0 specification

### **Testing & Examples**
- `test_generator.py` - Tests for simple API generator
- `test_universal_generator.py` - Tests for universal API generator
- `example_usage.py` - Example usage of the generators
- `example_endpoints.txt` - Example endpoints file for custom analysis

### **Configuration**
- `requirements.txt` - Python dependencies
- `guide.md` - Original NBA API guide and documentation
- `demo/` - Demo files and examples

### **Output Files**
- `analysis.json` - Generated API analysis (will be created when running generators)

## 🚀 **Quick Start**

### **Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Generate API Documentation**

#### **Method 1: Broad Discovery (Original)**
```bash
# Universal generator - discovers endpoints automatically
python3 universal_api_generator.py https://api.example.com

# Generate Swagger specification
python3 universal_api_generator.py https://api.example.com --swagger
```

#### **Method 2: Custom Endpoints (More Efficient)**
```bash
# Specify endpoints directly
python3 universal_api_generator.py https://api.example.com -e /users /posts /comments

# Use endpoints from file
python3 universal_api_generator.py https://api.example.com -f example_endpoints.txt

# Generate Swagger with custom endpoints
python3 universal_api_generator.py https://api.example.com -e /users /posts --swagger
```

### **Test the Generators**
```bash
# Test simple generator
python3 test_generator.py

# Test universal generator
python3 test_universal_generator.py

# Run examples
python3 example_usage.py
```

## 📋 **Available Commands**

### **Universal API Generator**
```bash
# Basic analysis with broad discovery
python3 universal_api_generator.py <api_url>

# Custom endpoints (more efficient)
python3 universal_api_generator.py <api_url> -e <endpoint1> <endpoint2> <endpoint3>

# Endpoints from file
python3 universal_api_generator.py <api_url> -f <endpoints_file.txt>

# Generate Swagger specification
python3 universal_api_generator.py <api_url> --swagger

# Custom output file
python3 universal_api_generator.py <api_url> -o <output.json>

# Custom timeout and delay
python3 universal_api_generator.py <api_url> -t 15 -d 0.2
```

### **Simple API Generator**
```bash
python3 simple_api_generator.py <api_url>
```

### **Swagger Generator**
```bash
python3 swagger_generator.py analysis.json
```

## 🎯 **Features**

### **Advanced Endpoint Discovery**
- **Broad Discovery**: Automatically discovers endpoints using common patterns
- **Custom Endpoints**: Specify exact endpoints for efficient analysis
- **OpenAPI/Swagger Integration**: Extracts endpoints from API specifications
- **Documentation Parsing**: Finds endpoints in API documentation pages

### **Enhanced Endpoint Validation**
- **Conservative Approach**: Only considers 200 status codes as healthy responses
- **Core HTTP Methods**: Tests only GET, POST, and DELETE methods
- **Reliable Discovery**: Focuses on endpoints that return successful responses
- **Detailed Logging**: Provides clear explanations for validation decisions

### **Comprehensive Analysis**
- **HTTP Method Discovery**: Identifies supported HTTP methods for each endpoint
- **Parameter Analysis**: Tests parameter variations and validation rules
- **Response Schema Inference**: Analyzes response structures and data types
- **CRUD Operation Detection**: Identifies Create, Read, Update, Delete operations
- **Error Response Mapping**: Documents various error scenarios

### **Custom Endpoints Feature**
- **Efficient Analysis**: Skip broad discovery for faster, targeted analysis
- **File Support**: Load endpoints from text files
- **Command Line Integration**: Specify endpoints directly via command line
- **Resource Optimization**: Reduce API calls and analysis time

## 🎯 **Custom Endpoints Feature**

### **Why Use Custom Endpoints?**
- **More Efficient**: Only tests specified endpoints instead of 50+ patterns
- **Faster Analysis**: Reduces API calls and processing time
- **Targeted Results**: Focus on specific endpoints you care about
- **Resource Friendly**: Less load on the target API
- **Predictable**: Know exactly which endpoints will be analyzed

### **How to Use Custom Endpoints**

#### **1. Command Line Arguments**
```bash
# Specify endpoints directly
python3 universal_api_generator.py https://api.example.com -e /users /posts /comments /albums

# Endpoints can be with or without leading slash
python3 universal_api_generator.py https://api.example.com -e users posts comments
```

#### **2. Endpoints File**
Create a text file with one endpoint per line:
```txt
# example_endpoints.txt
/users
/posts
/comments
/albums
/photos
```

Then use it:
```bash
python3 universal_api_generator.py https://api.example.com -f example_endpoints.txt
```

#### **3. Programmatic Usage**
```python
from universal_api_generator import UniversalAPIGenerator

# Define custom endpoints
custom_endpoints = ['/users', '/posts', '/comments']

# Create generator with custom endpoints
generator = UniversalAPIGenerator(
    base_url="https://api.example.com",
    custom_endpoints=custom_endpoints
)

# Generate analysis
analysis = generator.generate_analysis()
```

## 🔄 **Workflow**

### **Broad Discovery Workflow**
1. **Run Generator**: `python3 universal_api_generator.py https://api.example.com`
2. **Generate Analysis**: Creates `analysis.json` with discovered endpoints
3. **Generate Swagger**: `python3 universal_api_generator.py https://api.example.com --swagger`
4. **Copy to Frontend**: Copy `swagger.json` to `../universal_api_frontend/public/`

### **Custom Endpoints Workflow**
1. **Define Endpoints**: Create list or file of specific endpoints
2. **Run Generator**: `python3 universal_api_generator.py https://api.example.com -e /users /posts`
3. **Generate Analysis**: Creates `analysis.json` with targeted endpoints
4. **Generate Swagger**: `python3 universal_api_generator.py https://api.example.com -e /users /posts --swagger`
5. **Copy to Frontend**: Copy `swagger.json` to `../universal_api_frontend/public/`

## 📊 **Output Structure**

### **analysis.json**
```json
{
  "metadata": {
    "generator": "UniversalAPIGenerator",
    "version": "1.0.0",
    "base_url": "https://api.example.com",
    "custom_endpoints": true,
    "total_patterns_tested": 0
  },
  "summary": {
    "total_endpoints": 3,
    "crud_operations": {
      "create": 1,
      "read": 3,
      "update": 1,
      "delete": 1
    }
  },
  "endpoints": {
    "/users": {
      "methods": ["GET", "POST"],
      "parameters": {...},
      "response_schema": {...}
    }
  }
}
```

### **swagger.json**
OpenAPI 3.0 specification file ready for Swagger UI.

## 🛠️ **Customization**

- Modify `universal_api_generator.py` to add new endpoint patterns
- Update `swagger_generator.py` to customize OpenAPI output
- Add new parameter types in the generators
- Create custom endpoints files for different APIs

## 📝 **Notes**

- The backend generates `analysis.json` and `swagger.json` files
- Copy `swagger.json` to the frontend's `public/` folder for display
- Custom endpoints are more efficient than broad discovery
- Use `example_endpoints.txt` as a template for your own endpoints files
