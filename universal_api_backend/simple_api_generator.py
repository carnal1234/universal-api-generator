#!/usr/bin/env python3
"""
Simple Universal API Generator
Discovers CRUD endpoints and generates analysis JSON
"""

import requests
import json
import re
import time
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Any, Optional
import argparse


class SimpleAPIGenerator:
    def __init__(self, base_url: str, timeout: int = 10, delay: float = 0.1):
        """
        Initialize the API generator
        
        Args:
            base_url: Base URL of the API
            timeout: Request timeout in seconds
            delay: Delay between requests to be respectful
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SimpleAPIGenerator/1.0',
            'Accept': 'application/json'
        })
        
        # Common CRUD patterns
        self.crud_patterns = [
            # RESTful patterns
            '/users', '/posts', '/products', '/orders', '/items',
            '/customers', '/employees', '/articles', '/comments',
            # API versioned patterns
            '/api/users', '/api/v1/users', '/v1/users', '/v2/users',
            '/api/posts', '/api/v1/posts', '/v1/posts',
            # Common resource patterns
            '/data/users', '/data/posts', '/resources/users',
            # Generic patterns
            '/entities', '/objects', '/records'
        ]
        
        # Common parameters to test
        self.common_params = {
            'page': '1',
            'limit': '10',
            'per_page': '10',
            'size': '10',
            'offset': '0',
            'skip': '0',
            'sort': 'id',
            'order': 'asc',
            'filter': 'active',
            'status': 'active',
            'search': 'test',
            'q': 'test',
            'query': 'test',
            'fields': 'id,name',
            'include': 'details',
            'expand': 'true'
        }

    def discover_endpoints(self) -> List[str]:
        """
        Discover available endpoints using common patterns
        """
        print(f"🔍 Discovering endpoints for {self.base_url}")
        discovered_endpoints = []
        
        # Test common CRUD patterns
        for pattern in self.crud_patterns:
            url = urljoin(self.base_url, pattern)
            try:
                response = self.session.get(url, timeout=self.timeout)
                if self._is_valid_endpoint(response):
                    discovered_endpoints.append(pattern)
                    print(f"  ✅ Found: {pattern}")
                time.sleep(self.delay)
            except Exception as e:
                print(f"  ❌ Error testing {pattern}: {e}")
                continue
        
        # Try OpenAPI/Swagger if available
        openapi_endpoints = self._discover_with_openapi()
        discovered_endpoints.extend(openapi_endpoints)
        
        print(f"📊 Discovered {len(discovered_endpoints)} endpoints")
        return list(set(discovered_endpoints))  # Remove duplicates

    def _discover_with_openapi(self) -> List[str]:
        """
        Try to discover endpoints using OpenAPI/Swagger specification
        """
        openapi_urls = [
            '/openapi.json',
            '/swagger.json',
            '/api-docs',
            '/swagger/v1/swagger.json',
            '/v1/swagger.json',
            '/api-docs/v2/swagger.json'
        ]
        
        for openapi_path in openapi_urls:
            try:
                url = urljoin(self.base_url, openapi_path)
                response = self.session.get(url, timeout=self.timeout)
                if response.status_code == 200:
                    spec = response.json()
                    endpoints = self._parse_openapi_spec(spec)
                    print(f"  📋 Found OpenAPI spec, extracted {len(endpoints)} endpoints")
                    return endpoints
            except:
                continue
        
        return []

    def _parse_openapi_spec(self, spec: Dict) -> List[str]:
        """
        Parse OpenAPI specification to extract endpoints
        """
        endpoints = []
        
        if 'paths' in spec:
            for path, methods in spec['paths'].items():
                if path.startswith('/'):
                    endpoints.append(path)
        
        return endpoints

    def _is_valid_endpoint(self, response: requests.Response) -> bool:
        """
        Check if response indicates a valid endpoint
        """
        # Valid responses: 200 (success), 401 (unauthorized), 403 (forbidden)
        # Invalid: 404 (not found), 500 (server error)
        return response.status_code in [200, 401, 403, 405]  # 405 = method not allowed

    def analyze_endpoint(self, endpoint: str) -> Dict[str, Any]:
        """
        Analyze a single endpoint for parameters and behavior
        """
        print(f"🔬 Analyzing endpoint: {endpoint}")
        
        analysis = {
            'endpoint': endpoint,
            'methods': self._discover_methods(endpoint),
            'parameters': {},
            'response_schema': {},
            'error_responses': {},
            'crud_operations': self._identify_crud_operations(endpoint),
            'status': 'success'
        }
        
        # Analyze parameters for each method
        for method in analysis['methods']:
            method_analysis = self._analyze_method(endpoint, method)
            analysis['parameters'][method] = method_analysis['parameters']
            analysis['response_schema'][method] = method_analysis['response_schema']
            analysis['error_responses'][method] = method_analysis['error_responses']
        
        return analysis

    def _discover_methods(self, endpoint: str) -> List[str]:
        """
        Discover supported HTTP methods for an endpoint
        """
        methods = ['GET']
        
        # Test common CRUD methods
        test_methods = ['POST', 'PUT', 'PATCH', 'DELETE']
        url = urljoin(self.base_url, endpoint)
        
        for method in test_methods:
            try:
                response = self.session.request(method, url, timeout=self.timeout)
                if response.status_code not in [404, 405]:  # Method not found/not allowed
                    methods.append(method)
                time.sleep(self.delay)
            except:
                continue
        
        return methods

    def _analyze_method(self, endpoint: str, method: str) -> Dict[str, Any]:
        """
        Analyze parameters and responses for a specific HTTP method
        """
        url = urljoin(self.base_url, endpoint)
        
        analysis = {
            'parameters': {},
            'response_schema': {},
            'error_responses': {}
        }
        
        # Test with no parameters first
        try:
            response = self.session.request(method, url, timeout=self.timeout)
            analysis['error_responses']['no_params'] = {
                'status_code': response.status_code,
                'body': self._safe_json(response)
            }
            time.sleep(self.delay)
        except Exception as e:
            analysis['error_responses']['no_params'] = {
                'error': str(e)
            }
        
        # Test common parameters
        for param_name, param_value in self.common_params.items():
            try:
                params = {param_name: param_value}
                response = self.session.request(method, url, params=params, timeout=self.timeout)
                
                param_analysis = self._analyze_parameter_response(response, param_name, param_value)
                if param_analysis:
                    analysis['parameters'][param_name] = param_analysis
                
                time.sleep(self.delay)
            except Exception as e:
                continue
        
        # Analyze successful response schema
        if method == 'GET':
            try:
                response = self.session.get(url, timeout=self.timeout)
                if response.status_code == 200:
                    analysis['response_schema'] = self._analyze_response_schema(response)
            except:
                pass
        
        return analysis

    def _analyze_parameter_response(self, response: requests.Response, param_name: str, param_value: str) -> Optional[Dict]:
        """
        Analyze response to determine parameter behavior
        """
        if response.status_code == 400:
            # Parameter was accepted but invalid - extract error info
            error_info = self._extract_parameter_error(response, param_name)
            return {
                'type': 'string',  # Default assumption
                'required': False,  # Default assumption
                'error_response': error_info,
                'tested_value': param_value
            }
        elif response.status_code in [200, 401, 403]:
            # Parameter was accepted
            return {
                'type': 'string',
                'required': False,
                'accepted': True,
                'tested_value': param_value
            }
        
        return None

    def _extract_parameter_error(self, response: requests.Response, param_name: str) -> Dict:
        """
        Extract parameter validation error information
        """
        try:
            error_data = self._safe_json(response)
            return {
                'status_code': response.status_code,
                'body': error_data,
                'parameter_name': param_name
            }
        except:
            return {
                'status_code': response.status_code,
                'body': response.text[:500],  # First 500 chars
                'parameter_name': param_name
            }

    def _analyze_response_schema(self, response: requests.Response) -> Dict:
        """
        Analyze response structure to infer schema
        """
        try:
            data = self._safe_json(response)
            if isinstance(data, dict):
                return self._infer_object_schema(data)
            elif isinstance(data, list) and data:
                return {
                    'type': 'array',
                    'items': self._infer_object_schema(data[0])
                }
            else:
                return {'type': type(data).__name__}
        except:
            return {'type': 'unknown'}

    def _infer_object_schema(self, obj: Dict) -> Dict:
        """
        Infer schema from object structure
        """
        schema = {
            'type': 'object',
            'properties': {},
            'required': []
        }
        
        for key, value in obj.items():
            schema['properties'][key] = {
                'type': self._infer_type(value)
            }
        
        return schema

    def _infer_type(self, value: Any) -> str:
        """
        Infer data type from value
        """
        if isinstance(value, bool):
            return 'boolean'
        elif isinstance(value, int):
            return 'integer'
        elif isinstance(value, float):
            return 'number'
        elif isinstance(value, str):
            return 'string'
        elif isinstance(value, list):
            return 'array'
        elif isinstance(value, dict):
            return 'object'
        else:
            return 'string'

    def _identify_crud_operations(self, endpoint: str) -> Dict[str, bool]:
        """
        Identify CRUD operations based on endpoint pattern
        """
        endpoint_lower = endpoint.lower()
        
        # Extract resource name from endpoint
        resource_match = re.search(r'/([^/]+)(?:/([^/]+))?$', endpoint)
        if not resource_match:
            return {'create': False, 'read': False, 'update': False, 'delete': False}
        
        resource = resource_match.group(1)
        has_id = resource_match.group(2) is not None
        
        # Simple CRUD pattern detection
        crud_ops = {
            'create': not has_id,  # POST to /resource
            'read': True,          # GET to /resource or /resource/{id}
            'update': has_id,      # PUT/PATCH to /resource/{id}
            'delete': has_id       # DELETE to /resource/{id}
        }
        
        return crud_ops

    def _safe_json(self, response: requests.Response) -> Any:
        """
        Safely parse JSON response
        """
        try:
            return response.json()
        except:
            return response.text

    def generate_analysis(self) -> Dict[str, Any]:
        """
        Generate complete API analysis
        """
        print("🚀 Starting API analysis...")
        
        # Discover endpoints
        endpoints = self.discover_endpoints()
        
        if not endpoints:
            print("❌ No endpoints discovered")
            return {
                'status': 'error',
                'message': 'No endpoints discovered',
                'base_url': self.base_url
            }
        
        # Analyze each endpoint
        endpoint_analyses = {}
        for endpoint in endpoints:
            try:
                analysis = self.analyze_endpoint(endpoint)
                endpoint_analyses[endpoint] = analysis
            except Exception as e:
                print(f"❌ Error analyzing {endpoint}: {e}")
                endpoint_analyses[endpoint] = {
                    'endpoint': endpoint,
                    'status': 'error',
                    'error': str(e)
                }
        
        # Generate summary
        summary = self._generate_summary(endpoints, endpoint_analyses)
        
        analysis_result = {
            'metadata': {
                'generator': 'SimpleAPIGenerator',
                'version': '1.0.0',
                'generated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'base_url': self.base_url
            },
            'summary': summary,
            'endpoints': endpoint_analyses
        }
        
        print(f"✅ Analysis complete! Analyzed {len(endpoints)} endpoints")
        return analysis_result

    def _generate_summary(self, endpoints: List[str], analyses: Dict) -> Dict:
        """
        Generate summary statistics
        """
        total_endpoints = len(endpoints)
        successful_analyses = sum(1 for a in analyses.values() if a.get('status') == 'success')
        
        # Count CRUD operations
        crud_counts = {'create': 0, 'read': 0, 'update': 0, 'delete': 0}
        for analysis in analyses.values():
            if 'crud_operations' in analysis:
                for op, supported in analysis['crud_operations'].items():
                    if supported:
                        crud_counts[op] += 1
        
        # Count parameters
        total_params = 0
        param_types = {}
        for analysis in analyses.values():
            if 'parameters' in analysis:
                for method_params in analysis['parameters'].values():
                    total_params += len(method_params)
                    for param_name, param_info in method_params.items():
                        param_type = param_info.get('type', 'unknown')
                        param_types[param_type] = param_types.get(param_type, 0) + 1
        
        return {
            'total_endpoints': total_endpoints,
            'successful_analyses': successful_analyses,
            'crud_operations': crud_counts,
            'total_parameters': total_params,
            'parameter_types': param_types
        }

    def save_analysis(self, analysis: Dict, filename: str = 'analysis.json'):
        """
        Save analysis to JSON file
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        print(f"💾 Analysis saved to {filename}")


def main():
    parser = argparse.ArgumentParser(description='Simple Universal API Generator')
    parser.add_argument('base_url', help='Base URL of the API to analyze')
    parser.add_argument('-o', '--output', default='analysis.json', 
                       help='Output filename (default: analysis.json)')
    parser.add_argument('-t', '--timeout', type=int, default=10,
                       help='Request timeout in seconds (default: 10)')
    parser.add_argument('-d', '--delay', type=float, default=0.1,
                       help='Delay between requests in seconds (default: 0.1)')
    
    args = parser.parse_args()
    
    # Create generator
    generator = SimpleAPIGenerator(
        base_url=args.base_url,
        timeout=args.timeout,
        delay=args.delay
    )
    
    # Generate analysis
    analysis = generator.generate_analysis()
    
    # Save to file
    generator.save_analysis(analysis, args.output)
    
    # Print summary
    print("\n📊 Analysis Summary:")
    print(f"  Base URL: {analysis['metadata']['base_url']}")
    print(f"  Endpoints: {analysis['summary']['total_endpoints']}")
    print(f"  CRUD Operations:")
    for op, count in analysis['summary']['crud_operations'].items():
        print(f"    {op.capitalize()}: {count}")
    print(f"  Parameters: {analysis['summary']['total_parameters']}")


if __name__ == '__main__':
    main()
