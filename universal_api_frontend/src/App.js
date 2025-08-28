import React, { useState, useEffect } from "react";
import SwaggerUI from "swagger-ui-react";
import "swagger-ui-react/swagger-ui.css";
import { componentStyles } from "./styles";

function App() {
  const [url, setUrl] = useState("");
  const [customEndpoints, setCustomEndpoints] = useState("");
  const [apiDescription, setApiDescription] = useState("");
  const [apiName, setApiName] = useState("");
  const [showAdvancedOptions, setShowAdvancedOptions] = useState(false);
  const [swaggerSpec, setSwaggerSpec] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisProgress, setAnalysisProgress] = useState("");
  const [showHomeScreen, setShowHomeScreen] = useState(true);

  // Try to load existing swagger.json on component mount
  useEffect(() => {
    loadExistingSwagger();
  }, []);

  const loadExistingSwagger = async () => {
    try {
      const response = await fetch('/swagger.json');
      if (response.ok) {
        const spec = await response.json();
        setSwaggerSpec(spec);
        setShowHomeScreen(false);
        console.log('✅ Loaded existing swagger.json');
      }
    } catch (err) {
      console.log('ℹ️ No existing swagger.json found');
    }
  };

  const handleUrlSubmit = async (e) => {
    e.preventDefault();
    if (!url.trim()) return;

    setIsAnalyzing(true);
    setLoading(true);
    setError(null);
    setSwaggerSpec(null);
    setAnalysisProgress("Starting API analysis...");

    try {
      // Simulate the analysis process with progress updates
      setAnalysisProgress("Discovering endpoints...");
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setAnalysisProgress("Analyzing parameters...");
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setAnalysisProgress("Generating Swagger specification...");
      await new Promise(resolve => setTimeout(resolve, 1000));

      setAnalysisProgress("Analysis complete!");
      
      setError(null);
      setAnalysisProgress("");
      setLoading(false);
      
      // Call the backend API to generate swagger documentation
      try {
        setAnalysisProgress("Calling backend API...");
        
        const requestData = {
          url: url,
          customEndpoints: customEndpoints,
          apiName: apiName,
          apiDescription: apiDescription
        };
        
        const response = await fetch('/api/generate', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        if (data.success && data.swagger) {
          setSwaggerSpec(data.swagger);
          setShowHomeScreen(false);
          console.log('✅ Swagger spec generated successfully');
        } else {
          throw new Error(data.error || 'Failed to generate swagger specification');
        }
        
      } catch (apiError) {
        console.error('API Error:', apiError);
        setError(`Failed to generate API documentation: ${apiError.message}`);
        setAnalysisProgress("");
        setLoading(false);
      }
      
      // Generate command based on user input
      let command = `cd ../universal_api_backend\npython3 universal_api_generator.py "${url}" --swagger`;
      
      if (customEndpoints.trim()) {
        const endpoints = customEndpoints.split('\n')
          .map(line => line.trim())
          .filter(line => line && !line.startsWith('#'))
          .join(' ');
        command = `cd ../universal_api_backend\npython3 universal_api_generator.py "${url}" -e ${endpoints} --swagger`;
      }
      
      // Show instructions with custom endpoints if provided
      const message = customEndpoints.trim() 
        ? `To analyze ${url} with custom endpoints, run this command in your terminal:\n\n${command}\n\nThen copy swagger.json to ../universal_api_frontend/public/ and refresh this page.`
        : `To analyze ${url}, run this command in your terminal:\n\n${command}\n\nFor more efficient analysis with custom endpoints, add them in the advanced options above.\n\nThen copy swagger.json to ../universal_api_frontend/public/ and refresh this page.`;
      
      // alert(message);
      //TODO: fetch call the python script 
      
    } catch (err) {
      setError('Failed to analyze API. Please check the URL and try again.');
      setAnalysisProgress("");
      setLoading(false);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const spec = JSON.parse(e.target.result);
          setSwaggerSpec(spec);
          setError(null);
          setUrl("");
          setCustomEndpoints("");
          setApiDescription("");
          setApiName("");
          setShowHomeScreen(false);
          console.log('✅ Swagger spec loaded from file');
        } catch (err) {
          setError('Invalid JSON file');
          console.error('❌ Error parsing JSON:', err);
        }
      };
      reader.readAsText(file);
    }
  };

  const resetAnalysis = () => {
    setSwaggerSpec(null);
    setError(null);
    setUrl("");
    setCustomEndpoints("");
    setApiDescription("");
    setApiName("");
    setShowAdvancedOptions(false);
    setAnalysisProgress("");
    setShowHomeScreen(true);
  };

  const handleExampleClick = (exampleUrl, exampleEndpoints = "", exampleName = "") => {
    setUrl(exampleUrl);
    if (exampleEndpoints) {
      setCustomEndpoints(exampleEndpoints);
      setShowAdvancedOptions(true);
    }
    if (exampleName) {
      setApiName(exampleName);
    }
  };

  // Home Screen - Enhanced with Tailwind CSS
  if (showHomeScreen) {
    return (
      <div className={componentStyles.homeScreen.container}>
        <div className={componentStyles.homeScreen.mainContent}>
          <div className={componentStyles.homeScreen.contentWrapper}>
            {/* Header */}
            <div className={componentStyles.homeScreen.header}>
              <h1 className={componentStyles.homeScreen.title}>
                Universal API Generator
              </h1>
              <p className={componentStyles.homeScreen.subtitle}>
                Discover and document any REST API automatically
              </p>
            </div>

            {/* URL Input Form */}
            <form onSubmit={handleUrlSubmit} className={componentStyles.homeScreen.form}>
              <div className={componentStyles.homeScreen.inputWrapper}>
                <input
                  type="url"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="https://api.example.com"
                  className={componentStyles.homeScreen.urlInput}
                  disabled={loading}
                  required
                />
                <button
                  type="submit"
                  disabled={!url.trim() || loading}
                  className={componentStyles.homeScreen.submitButton}
                >
                  {loading ? (
                    <>
                      <span className="animate-spin">⏳</span>
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <span>🔍</span>
                      Analyze API
                    </>
                  )}
                </button>
              </div>
            </form>

            {/* Advanced Options Toggle */}
            <div className="mb-4">
              <button
                type="button"
                onClick={() => setShowAdvancedOptions(!showAdvancedOptions)}
                className={componentStyles.homeScreen.advancedToggle}
              >
                {showAdvancedOptions ? '▼ Hide' : '▶ Show'} Advanced Options
              </button>
            </div>

            {/* Advanced Options */}
            {showAdvancedOptions && (
              <div className={componentStyles.homeScreen.advancedPanel}>
                <h3 className={componentStyles.homeScreen.advancedTitle}>
                  Advanced Options
                </h3>
                
                {/* API Name */}
                <div className="mb-4">
                  <label className={componentStyles.homeScreen.label}>
                    API Name (Optional)
                  </label>
                  <input
                    type="text"
                    value={apiName}
                    onChange={(e) => setApiName(e.target.value)}
                    placeholder="My Awesome API"
                    className="w-full p-3 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                
                {/* API Description */}
                <div className="mb-4">
                  <label className={componentStyles.homeScreen.label}>
                    API Description (Optional)
                  </label>
                  <textarea
                    value={apiDescription}
                    onChange={(e) => setApiDescription(e.target.value)}
                    placeholder="Describe the API or add any additional context..."
                    className={componentStyles.homeScreen.textarea}
                  />
                </div>

                {/* Custom Endpoints */}
                <div className="mb-4">
                  <label className={componentStyles.homeScreen.label}>
                    Custom Endpoints (Optional)
                  </label>
                  <textarea
                    value={customEndpoints}
                    onChange={(e) => setCustomEndpoints(e.target.value)}
                    placeholder={`Enter specific endpoints to analyze (one per line):
/users
/posts
/comments
# Lines starting with # are comments`}
                    className={componentStyles.homeScreen.textareaMonospace}
                  />
                  <p className={componentStyles.homeScreen.helpText}>
                    💡 Tip: Specifying custom endpoints makes analysis faster and more efficient
                  </p>
                </div>
              </div>
            )}

            {/* Progress Bar */}
            {isAnalyzing && (
              <div className={componentStyles.homeScreen.progressContainer}>
                <div className={componentStyles.homeScreen.progressBar}>
                  <div className={componentStyles.homeScreen.progressFill}></div>
                </div>
                <p className={componentStyles.homeScreen.progressText}>
                  {analysisProgress}
                </p>
              </div>
            )}

            {/* Error Message */}
            {error && (
              <div className={componentStyles.homeScreen.errorContainer}>
                <span className="text-xl">⚠️</span>
                {error}
              </div>
            )}

            {/* Alternative Options */}
            <div className="mb-8">
              <div className={componentStyles.homeScreen.divider}>
                <span className={componentStyles.homeScreen.dividerText}>
                  or
                </span>
              </div>
              
              <div className={componentStyles.homeScreen.fileUpload}>
                <label className="cursor-pointer">
                  <input
                    type="file"
                    accept=".json"
                    onChange={handleFileUpload}
                    className="hidden"
                  />
                  <span className={componentStyles.homeScreen.fileUploadButton}>
                    📁 Upload Swagger JSON
                  </span>
                </label>
                <p className={componentStyles.homeScreen.fileUploadText}>
                  Upload an existing swagger.json file
                </p>
              </div>
            </div>

            {/* Example APIs */}
            <div className={componentStyles.homeScreen.examplesContainer}>
              <h3 className={componentStyles.homeScreen.examplesTitle}>
                Try these example APIs:
              </h3>
              <div className={componentStyles.homeScreen.examplesGrid}>
                <button 
                  onClick={() => handleExampleClick(
                    "https://jsonplaceholder.typicode.com", 
                    "/users\n/posts\n/comments\n/albums\n/photos",
                    "JSONPlaceholder"
                  )}
                  className={componentStyles.homeScreen.exampleButton}
                >
                  JSONPlaceholder
                </button>
                <button 
                  onClick={() => handleExampleClick(
                    "https://api.github.com", 
                    "/users\n/repos\n/orgs\n/events",
                    "GitHub API"
                  )}
                  className={componentStyles.homeScreen.exampleButton}
                >
                  GitHub API
                </button>
                <button 
                  onClick={() => handleExampleClick(
                    "https://dogapi.dog", 
                    "/v1/breeds\n/v1/facts\n/v1/images",
                    "Dog API"
                  )}
                  className={componentStyles.homeScreen.exampleButton}
                >
                  Dog API
                </button>
                <button 
                  onClick={() => handleExampleClick(
                    "https://pokeapi.co", 
                    "/api/v2/pokemon\n/api/v2/ability\n/api/v2/type",
                    "PokéAPI"
                  )}
                  className={componentStyles.homeScreen.exampleButton}
                >
                  PokéAPI
                </button>
                <button 
                  onClick={() => handleExampleClick(
                    "https://api.openf1.org/v1", 
                    "/drivers\n/constructors\n/races\n/results",
                    "OpenF1 API"
                  )}
                  className={componentStyles.homeScreen.exampleButton}
                >
                  OpenF1 API
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Swagger UI View
  return (
    <div className={componentStyles.swaggerView.container}>
      <div className={componentStyles.swaggerView.header}>
        <h1 className={componentStyles.swaggerView.title}>
          {apiName || "API Documentation"}
        </h1>
        <button onClick={resetAnalysis} className={componentStyles.swaggerView.resetButton}>
          🔄 New Analysis
        </button>
      </div>
      
      {swaggerSpec ? (
        <SwaggerUI spec={swaggerSpec} />
      ) : (
        <div className="text-center py-12">
          <p className="text-gray-600">No API documentation loaded</p>
        </div>
      )}
    </div>
  );
}

export default App;