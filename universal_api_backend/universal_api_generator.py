#!/usr/bin/env python3
"""
Universal API Generator
A simplified but powerful API generator inspired by the NBA API system
"""

import json
import requests
import re
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from urllib.parse import urljoin
import argparse
# Removed code_generator import - no longer needed


class UniversalAPIGenerator:
    def __init__(self, base_url: str, custom_endpoints: List[str] = None, timeout: int = 10, delay: float = 0.1):
        """
        Initialize the Universal API Generator
        
        Args:
            base_url: Base URL of the API to analyze
            custom_endpoints: Optional list of specific endpoints to analyze (more efficient than broad discovery)
            timeout: Request timeout in seconds
            delay: Delay between requests to be respectful
        """
        self.base_url = base_url.rstrip('/')
        self.custom_endpoints = custom_endpoints
        self.timeout = timeout
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'UniversalAPIGenerator/1.0',
            'Accept': 'application/json'
        })
        
        # Universal endpoint patterns (more comprehensive than simple version)
        self.endpoint_patterns = [
            # RESTful resources
            '/users', '/posts', '/products', '/orders', '/items', '/customers',
            '/employees', '/articles', '/comments', '/reviews', '/ratings',
            '/categories', '/tags', '/files', '/images', '/documents',
            '/projects', '/tasks', '/events', '/schedules', '/bookings',
            '/payments', '/invoices', '/transactions', '/accounts', '/profiles',
            
            # API versioned patterns
            '/api/users', '/api/v1/users', '/api/v2/users', '/v1/users', '/v2/users',
            '/api/posts', '/api/v1/posts', '/api/v2/posts', '/v1/posts',
            '/api/products', '/api/v1/products', '/api/v2/products',
            
            # Common API patterns
            '/data/users', '/data/posts', '/resources/users', '/resources/posts',
            '/services/users', '/services/posts', '/entities/users', '/entities/posts',
            
            # Generic patterns
            '/entities', '/objects', '/records', '/items', '/data', '/resources',
            
            # Authentication and user management
            '/auth', '/login', '/logout', '/register', '/signup', '/signin',
            '/password', '/reset', '/verify', '/confirm', '/activate',
            
            # File and media
            '/files', '/uploads', '/downloads', '/media', '/images', '/videos',
            '/documents', '/attachments', '/assets', '/static',
            
            # Search and discovery
            '/search', '/find', '/query', '/discover', '/explore', '/browse',
            
            # Analytics and metrics
            '/analytics', '/metrics', '/stats', '/reports', '/dashboard',
            '/insights', '/data', '/statistics'
        ]
        
        # Comprehensive parameter testing
        self.parameter_variations = {
            # Pagination
            # 'page': {'default': '1', 'test_values': ['1', '2', '10'], 'error_value': 'abc'},
            # 'limit': {'default': '10', 'test_values': ['10', '20', '50'], 'error_value': 'abc'},
            # 'per_page': {'default': '10', 'test_values': ['10', '20', '50'], 'error_value': 'abc'},
            # 'size': {'default': '10', 'test_values': ['10', '20', '50'], 'error_value': 'abc'},
            # 'offset': {'default': '0', 'test_values': ['0', '10', '20'], 'error_value': 'abc'},
            # 'skip': {'default': '0', 'test_values': ['0', '10', '20'], 'error_value': 'abc'},
            
            # Sorting
            # 'sort': {'default': 'id', 'test_values': ['id', 'name', 'created_at'], 'error_value': 'invalid'},
            # 'order': {'default': 'asc', 'test_values': ['asc', 'desc'], 'error_value': 'invalid'},
            # 'sort_by': {'default': 'id', 'test_values': ['id', 'name', 'created_at'], 'error_value': 'invalid'},
            # 'sort_order': {'default': 'asc', 'test_values': ['asc', 'desc'], 'error_value': 'invalid'},
            
            # Filtering
            # 'filter': {'default': 'active', 'test_values': ['active', 'inactive', 'all'], 'error_value': 'invalid'},
            # 'status': {'default': 'active', 'test_values': ['active', 'inactive', 'pending'], 'error_value': 'invalid'},
            # 'type': {'default': 'user', 'test_values': ['user', 'admin', 'moderator'], 'error_value': 'invalid'},
            # 'category': {'default': 'general', 'test_values': ['general', 'tech', 'news'], 'error_value': 'invalid'},
            
            # Search
            # 'search': {'default': 'test', 'test_values': ['test', 'example', 'demo'], 'error_value': ''},
            # 'q': {'default': 'test', 'test_values': ['test', 'example', 'demo'], 'error_value': ''},
            # 'query': {'default': 'test', 'test_values': ['test', 'example', 'demo'], 'error_value': ''},
            # 'keyword': {'default': 'test', 'test_values': ['test', 'example', 'demo'], 'error_value': ''},
            
            # Fields and includes
            # 'fields': {'default': 'id,name', 'test_values': ['id,name', 'id,email', 'all'], 'error_value': 'invalid'},
            # 'include': {'default': 'details', 'test_values': ['details', 'profile', 'settings'], 'error_value': 'invalid'},
            # 'expand': {'default': 'true', 'test_values': ['true', 'false'], 'error_value': 'invalid'},
            # 'select': {'default': 'id,name', 'test_values': ['id,name', 'id,email', 'all'], 'error_value': 'invalid'},
            
            # Date and time
            # 'date': {'default': '2024-01-01', 'test_values': ['2024-01-01', '2024-12-31'], 'error_value': 'invalid'},
            # 'from': {'default': '2024-01-01', 'test_values': ['2024-01-01', '2024-06-01'], 'error_value': 'invalid'},
            # 'to': {'default': '2024-12-31', 'test_values': ['2024-06-30', '2024-12-31'], 'error_value': 'invalid'},
            # 'since': {'default': '2024-01-01', 'test_values': ['2024-01-01', '2024-06-01'], 'error_value': 'invalid'},
            
            # IDs and references
            # 'id': {'default': '1', 'test_values': ['1', '2', '123'], 'error_value': 'invalid'},
            # 'user_id': {'default': '1', 'test_values': ['1', '2', '123'], 'error_value': 'invalid'},
            # 'post_id': {'default': '1', 'test_values': ['1', '2', '123'], 'error_value': 'invalid'},
            # 'category_id': {'default': '1', 'test_values': ['1', '2', '123'], 'error_value': 'invalid'},
            
            # Authentication
            # 'api_key': {'default': 'test_key', 'test_values': ['test_key', 'demo_key'], 'error_value': 'invalid'},
            # 'token': {'default': 'test_token', 'test_values': ['test_token', 'demo_token'], 'error_value': 'invalid'},
            # 'access_token': {'default': 'test_token', 'test_values': ['test_token', 'demo_token'], 'error_value': 'invalid'}
        }

    def discover_endpoints(self) -> List[str]:
        """Discover available endpoints using comprehensive patterns or custom list"""
        print(f"🔍 Discovering endpoints for {self.base_url}")
        
        # If custom endpoints are provided, use them directly (more efficient)
        if self.custom_endpoints:
            print(f"📋 Using custom endpoints list: {len(self.custom_endpoints)} endpoints")
            discovered_endpoints = []
            
            for endpoint in self.custom_endpoints:
                # Normalize endpoint format - handle both "meeting" and "/meeting"
                endpoint = endpoint.strip()
                if not endpoint.startswith('/'):
                    endpoint = '/' + endpoint
                
                # Fix URL construction - use direct concatenation instead of urljoin
                url = self.base_url + endpoint
                try:
                    response = self.session.get(url, timeout=self.timeout)
                    if self._is_valid_endpoint(response):
                        discovered_endpoints.append(endpoint)
                        reason = self._get_endpoint_validation_reason(response)
                        print(f"  ✅ Found: {endpoint} - {reason}")
                    else:
                        reason = self._get_endpoint_validation_reason(response)
                        print(f"  ⚠️  Not accessible: {endpoint} - {reason}")
                    time.sleep(self.delay)
                except Exception as e:
                    print(f"  ❌ Error testing {endpoint}: {e}")
                    continue
            
            print(f"📊 Discovered {len(discovered_endpoints)} endpoints from custom list")
            return discovered_endpoints
        
        # Otherwise, use the original broad discovery method
        discovered_endpoints = []
        
        # Test endpoint patterns
        for pattern in self.endpoint_patterns:
            url = self.base_url + pattern
            try:
                response = self.session.get(url, timeout=self.timeout)
                if self._is_valid_endpoint(response):
                    discovered_endpoints.append(pattern)
                    reason = self._get_endpoint_validation_reason(response)
                    print(f"  ✅ Found: {pattern} - {reason}")
                time.sleep(self.delay)
            except Exception as e:
                continue
        
        # Try OpenAPI/Swagger discovery
        openapi_endpoints = self._discover_with_openapi()
        discovered_endpoints.extend(openapi_endpoints)
        
        # Try common API documentation endpoints
        doc_endpoints = self._discover_from_documentation()
        discovered_endpoints.extend(doc_endpoints)
        
        print(f"📊 Discovered {len(discovered_endpoints)} endpoints")
        return list(set(discovered_endpoints))

    def _discover_with_openapi(self) -> List[str]:
        """Discover endpoints using OpenAPI/Swagger specifications"""
        openapi_urls = [
            '/openapi.json', '/swagger.json', '/api-docs',
            '/swagger/v1/swagger.json', '/v1/swagger.json',
            '/api-docs/v2/swagger.json', '/api/v1/swagger.json',
            '/docs/swagger.json', '/api/docs/swagger.json'
        ]
        
        for openapi_path in openapi_urls:
            try:
                url = self.base_url + openapi_path
                response = self.session.get(url, timeout=self.timeout)
                if response.status_code == 200:
                    spec = response.json()
                    endpoints = self._parse_openapi_spec(spec)
                    print(f"  📋 Found OpenAPI spec, extracted {len(endpoints)} endpoints")
                    return endpoints
            except:
                continue
        
        return []

    def _discover_from_documentation(self) -> List[str]:
        """Try to discover endpoints from common documentation URLs"""
        doc_urls = [
            '/docs', '/documentation', '/api-docs', '/api/documentation',
            '/help', '/api/help', '/reference', '/api/reference'
        ]
        
        discovered = []
        for doc_url in doc_urls:
            try:
                url = self.base_url + doc_url
                response = self.session.get(url, timeout=self.timeout)
                if response.status_code == 200:
                    # Try to extract endpoints from documentation page
                    endpoints = self._extract_endpoints_from_html(response.text)
                    if endpoints:
                        print(f"  📄 Found documentation, extracted {len(endpoints)} endpoints")
                        discovered.extend(endpoints)
            except:
                continue
        
        return discovered

    def _extract_endpoints_from_html(self, html_content: str) -> List[str]:
        """Extract endpoint patterns from HTML documentation"""
        endpoints = []
        
        # Common patterns in documentation
        patterns = [
            r'["\'](/api/[^"\']+)["\']',
            r'["\'](/v\d+/[^"\']+)["\']',
            r'["\'](/[a-z]+/[^"\']+)["\']',
            r'GET\s+([^\s]+)',
            r'POST\s+([^\s]+)',
            r'PUT\s+([^\s]+)',
            r'DELETE\s+([^\s]+)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            endpoints.extend(matches)
        
        return list(set(endpoints))

    def _parse_openapi_spec(self, spec: Dict) -> List[str]:
        """Parse OpenAPI specification to extract endpoints"""
        endpoints = []
        
        if 'paths' in spec:
            for path, methods in spec['paths'].items():
                if path.startswith('/'):
                    endpoints.append(path)
        
        return endpoints

    def _is_valid_endpoint(self, response: requests.Response) -> bool:
        """Check if response indicates a valid endpoint"""
        status = response.status_code
        
        # Definitely valid responses
        if status == 200:
            return True
        
        # Responses that indicate the endpoint exists but has issues
        # These are still valid endpoints, just with different access requirements
        valid_status_codes = [
            200,  # OK
            201,  # Created
            202,  # Accepted
            204,  # No Content
            401,  # Unauthorized (endpoint exists, needs auth)
            403,  # Forbidden (endpoint exists, access denied)
            405,  # Method Not Allowed (endpoint exists, wrong method)
            422,  # Unprocessable Entity (endpoint exists, bad request)
            429,  # Too Many Requests (endpoint exists, rate limited)
        ]
        
        return status in valid_status_codes

    def _get_endpoint_validation_reason(self, response: requests.Response) -> str:
        """Get a human-readable reason for endpoint validation decision"""
        status = response.status_code
        
        if status == 200:
            return "Endpoint exists and is accessible"
        elif status == 404:
            return "Endpoint does not exist"
        elif status == 401:
            return "Endpoint exists but requires authentication"
        elif status == 403:
            return "Endpoint exists but access is forbidden"
        elif status == 405:
            return "Endpoint exists but HTTP method not allowed"
        elif status == 422:
            return "Endpoint exists but request was malformed (e.g., too much data)"
        elif status == 400:
            return "Endpoint exists but request was invalid"
        elif status == 500:
            return "Endpoint exists but server encountered an error"
        elif status == 503:
            return "Endpoint exists but service is temporarily unavailable"
        else:
            return f"Endpoint may exist but returned status: {status}"

    def analyze_endpoint(self, endpoint: str) -> Dict[str, Any]:
        """Analyze a single endpoint comprehensively"""
        print(f"🔬 Analyzing endpoint: {endpoint}")
        
        analysis = {
            'endpoint': endpoint,
            'methods': self._discover_methods(endpoint),
            'parameters': {},
            'response_schema': {},
            'error_responses': {},
            'crud_operations': self._identify_crud_operations(endpoint),
            'parameter_validation': {},
            'status': 'success'
        }
        
        # Analyze each method
        for method in analysis['methods']:
            method_analysis = self._analyze_method_comprehensive(endpoint, method)
            analysis['parameters'][method] = method_analysis['parameters']
            analysis['response_schema'][method] = method_analysis['response_schema']
            analysis['error_responses'][method] = method_analysis['error_responses']
            analysis['parameter_validation'][method] = method_analysis['parameter_validation']
        
        return analysis

    def _discover_methods(self, endpoint: str) -> List[str]:
        """Discover supported HTTP methods for an endpoint"""
        methods = []
        
        # Only test GET and POST methods
        test_methods = ['GET', 'POST']
        url = self.base_url + endpoint
        
        for method in test_methods:
            try:
                response = self.session.request(method, url, timeout=self.timeout)
                # Use the enhanced _is_valid_endpoint logic
                if self._is_valid_endpoint(response):
                    methods.append(method)
                    reason = self._get_endpoint_validation_reason(response)
                    print(f"    ✅ {method} method supported - {reason}")
                else:
                    reason = self._get_endpoint_validation_reason(response)
                    print(f"    ❌ {method} method not supported - {reason}")
                time.sleep(self.delay)
            except Exception as e:
                print(f"    ⚠️ Error testing {method} method: {e}")
                continue
        
        # Always include GET if no methods were found (fallback)
        if not methods:
            methods = ['GET']
            print(f"    ⚠️ No methods discovered, defaulting to GET")
        
        return methods

    def _analyze_method_comprehensive(self, endpoint: str, method: str) -> Dict[str, Any]:
        """Comprehensive method analysis with parameter validation"""
        url = self.base_url + endpoint
        
        analysis = {
            'parameters': {},
            'response_schema': {},
            'error_responses': {},
            'parameter_validation': {}
        }
        
        # Test with no parameters
        try:
            response = self.session.request(method, url, timeout=self.timeout)
            analysis['error_responses']['no_params'] = {
                'status_code': response.status_code,
                'body': self._safe_json(response)
            }
            time.sleep(self.delay)
        except Exception as e:
            analysis['error_responses']['no_params'] = {'error': str(e)}
        
        # Test comprehensive parameter variations
        for param_name, param_info in self.parameter_variations.items():
            param_analysis = self._analyze_parameter_comprehensive(
                url, method, param_name, param_info
            )
            if param_analysis:
                analysis['parameters'][param_name] = param_analysis['parameter_info']
                analysis['parameter_validation'][param_name] = param_analysis['validation_info']
        
        # Analyze successful response schema
        if method == 'GET':
            try:
                response = self.session.get(url, timeout=self.timeout)
                if response.status_code == 200:
                    analysis['response_schema'] = self._analyze_response_schema_comprehensive(response)
            except:
                pass
        
        return analysis

    def _analyze_parameter_comprehensive(self, url: str, method: str, 
                                       param_name: str, param_info: Dict) -> Optional[Dict]:
        """Comprehensive parameter analysis with validation testing"""
        validation_info = {
            'accepted_values': [],
            'rejected_values': [],
            'validation_patterns': [],
            'required': False,
            'type': 'string'
        }
        
        # Test default value
        try:
            params = {param_name: param_info['default']}
            response = self.session.request(method, url, params=params, timeout=self.timeout)
            
            if response.status_code in [200, 401, 403]:
                validation_info['accepted_values'].append(param_info['default'])
            elif response.status_code == 400:
                validation_info['rejected_values'].append(param_info['default'])
            
            time.sleep(self.delay)
        except:
            pass
        
        # Test multiple values
        for test_value in param_info['test_values']:
            try:
                params = {param_name: test_value}
                response = self.session.request(method, url, params=params, timeout=self.timeout)
                
                if response.status_code in [200, 401, 403]:
                    validation_info['accepted_values'].append(test_value)
                elif response.status_code == 400:
                    validation_info['rejected_values'].append(test_value)
                
                time.sleep(self.delay)
            except:
                continue
        
        # Test error value
        try:
            params = {param_name: param_info['error_value']}
            response = self.session.request(method, url, params=params, timeout=self.timeout)
            
            if response.status_code == 400:
                validation_info['rejected_values'].append(param_info['error_value'])
                # Try to extract validation error message
                error_info = self._extract_validation_error(response, param_name)
                if error_info:
                    validation_info['validation_patterns'].append(error_info)
            
            time.sleep(self.delay)
        except:
            pass
        
        # Determine if parameter is required
        if validation_info['accepted_values'] and not validation_info['rejected_values']:
            validation_info['required'] = False
        elif validation_info['rejected_values'] and not validation_info['accepted_values']:
            validation_info['required'] = True
        
        # Infer parameter type
        validation_info['type'] = self._infer_parameter_type(validation_info['accepted_values'])
        
        return {
            'parameter_info': {
                'type': validation_info['type'],
                'required': validation_info['required'],
                'default': param_info['default'],
                'accepted': len(validation_info['accepted_values']) > 0
            },
            'validation_info': validation_info
        }

    def _extract_validation_error(self, response: requests.Response, param_name: str) -> Optional[str]:
        """Extract validation error message from response"""
        try:
            error_data = self._safe_json(response)
            if isinstance(error_data, dict):
                # Look for common error message patterns
                error_fields = ['error', 'message', 'detail', 'description']
                for field in error_fields:
                    if field in error_data:
                        error_msg = str(error_data[field])
                        if param_name.lower() in error_msg.lower():
                            return error_msg
        except:
            pass
        
        return None

    def _infer_parameter_type(self, accepted_values: List[str]) -> str:
        """Infer parameter type from accepted values"""
        if not accepted_values:
            return 'string'
        
        # Check if all values are integers
        if all(value.isdigit() for value in accepted_values):
            return 'integer'
        
        # Check if all values are booleans
        if all(value.lower() in ['true', 'false'] for value in accepted_values):
            return 'boolean'
        
        # Check if all values are dates
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if all(re.match(date_pattern, value) for value in accepted_values):
            return 'date'
        
        return 'string'

    def _analyze_response_schema_comprehensive(self, response: requests.Response) -> Dict:
        """Comprehensive response schema analysis"""
        try:
            data = self._safe_json(response)
            if isinstance(data, dict):
                return self._infer_object_schema_comprehensive(data)
            elif isinstance(data, list) and data:
                return {
                    'type': 'array',
                    'items': self._infer_object_schema_comprehensive(data[0]),
                    'count': len(data)
                }
            else:
                return {'type': type(data).__name__}
        except:
            return {'type': 'unknown'}

    def _infer_object_schema_comprehensive(self, obj: Dict) -> Dict:
        """Comprehensive object schema inference"""
        schema = {
            'type': 'object',
            'properties': {},
            'required': [],
            'example': obj
        }
        
        for key, value in obj.items():
            schema['properties'][key] = {
                'type': self._infer_type_comprehensive(value),
                'example': value
            }
        
        return schema

    def _infer_type_comprehensive(self, value: Any) -> str:
        """Comprehensive type inference"""
        if isinstance(value, bool):
            return 'boolean'
        elif isinstance(value, int):
            return 'integer'
        elif isinstance(value, float):
            return 'number'
        elif isinstance(value, str):
            # Try to infer more specific string types
            if re.match(r'^\d{4}-\d{2}-\d{2}', value):
                return 'date'
            elif re.match(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$', value):
                return 'uuid'
            elif '@' in value and '.' in value:
                return 'email'
            elif value.startswith('http'):
                return 'url'
            else:
                return 'string'
        elif isinstance(value, list):
            return 'array'
        elif isinstance(value, dict):
            return 'object'
        else:
            return 'string'

    def _identify_crud_operations(self, endpoint: str) -> Dict[str, bool]:
        """Identify CRUD operations based on endpoint pattern"""
        endpoint_lower = endpoint.lower()
        
        # Extract resource name from endpoint
        resource_match = re.search(r'/([^/]+)(?:/([^/]+))?$', endpoint)
        if not resource_match:
            return {'create': False, 'read': False, 'update': False, 'delete': False}
        
        resource = resource_match.group(1)
        has_id = resource_match.group(2) is not None
        
        # Enhanced CRUD pattern detection
        crud_ops = {
            'create': not has_id,  # POST to /resource
            'read': True,          # GET to /resource or /resource/{id}
            'update': has_id,      # PUT/PATCH to /resource/{id}
            'delete': has_id       # DELETE to /resource/{id}
        }
        
        # Special cases
        if 'auth' in endpoint_lower or 'login' in endpoint_lower:
            crud_ops = {'create': True, 'read': False, 'update': False, 'delete': False}
        elif 'search' in endpoint_lower or 'find' in endpoint_lower:
            crud_ops = {'create': False, 'read': True, 'update': False, 'delete': False}
        
        return crud_ops

    def _safe_json(self, response: requests.Response) -> Any:
        """Safely parse JSON response"""
        try:
            return response.json()
        except:
            return response.text

    def generate_analysis(self) -> Dict[str, Any]:
        """Generate complete API analysis"""
        print("🚀 Starting Universal API analysis...")
        
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
        
        # Generate comprehensive summary
        summary = self._generate_comprehensive_summary(endpoints, endpoint_analyses)
        
        analysis_result = {
            'metadata': {
                'generator': 'UniversalAPIGenerator',
                'version': '1.0.0',
                'generated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'base_url': self.base_url,
                'custom_endpoints': self.custom_endpoints is not None,
                'total_patterns_tested': len(self.endpoint_patterns) if not self.custom_endpoints else 0,
                'total_parameters_tested': len(self.parameter_variations)
            },
            'summary': summary,
            'endpoints': endpoint_analyses,
            'parameter_variations': self.parameter_variations
        }
        
        print(f"✅ Analysis complete! Analyzed {len(endpoints)} endpoints")
        return analysis_result

    def _generate_comprehensive_summary(self, endpoints: List[str], analyses: Dict) -> Dict:
        """Generate comprehensive summary statistics"""
        total_endpoints = len(endpoints)
        successful_analyses = sum(1 for a in analyses.values() if a.get('status') == 'success')
        
        # Count CRUD operations
        crud_counts = {'create': 0, 'read': 0, 'update': 0, 'delete': 0}
        for analysis in analyses.values():
            if 'crud_operations' in analysis:
                for op, supported in analysis['crud_operations'].items():
                    if supported:
                        crud_counts[op] += 1
        
        # Count parameters and validation
        total_params = 0
        param_types = {}
        validation_patterns = []
        
        for analysis in analyses.values():
            try:
                if 'parameters' in analysis:
                    for method_params in analysis['parameters'].values():
                        total_params += len(method_params)
                        for param_name, param_info in method_params.items():
                            param_type = param_info.get('type', 'unknown')
                            param_types[param_type] = param_types.get(param_type, 0) + 1
                
                if 'parameter_validation' in analysis:
                    for method_validation in analysis['parameter_validation'].values():
                        for param_name, validation_info in method_validation.items():
                            if validation_info.get('validation_patterns'):
                                validation_patterns.extend(validation_info['validation_patterns'])
            except Exception as e:
                print(f"⚠️ Warning: Error processing parameters for analysis: {e}")
                continue
        
        # Calculate discovery rate safely
        discovery_rate = "0.0%"
        if self.endpoint_patterns and len(self.endpoint_patterns) > 0:
            rate = (len(endpoints) / len(self.endpoint_patterns)) * 100
            discovery_rate = f"{rate:.1f}%"
        
        return {
            'total_endpoints': total_endpoints,
            'successful_analyses': successful_analyses,
            'crud_operations': crud_counts,
            'total_parameters': total_params,
            'parameter_types': param_types,
            'validation_patterns': list(set(validation_patterns)),
            'discovery_rate': discovery_rate
        }

    def save_analysis(self, analysis: Dict, filename: str = 'analysis.json'):
        """Save analysis to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        print(f"💾 Analysis saved to {filename}")

    def generate_swagger_spec(self, analysis_file: str = 'analysis.json'):
        """Generate Swagger specification from analysis"""
        print("📚 Generating Swagger specification...")
        
        try:
            from swagger_generator import SwaggerGenerator
            generator = SwaggerGenerator(analysis_file)
            output_file = generator.save_swagger_spec('swagger.json')
            
            if output_file:
                print("✅ Swagger specification generated successfully!")
                print(f"📄 File: {output_file}")
                print("🌐 Use this file with swagger-ui-react in your React app")
                return True
            else:
                print("❌ Failed to generate Swagger specification")
                return False
        except ImportError:
            print("❌ Swagger generator not available")
            return False


def main():
    parser = argparse.ArgumentParser(description='Universal API Generator')
    parser.add_argument('base_url', help='Base URL of the API to analyze')
    parser.add_argument('-e', '--endpoints', nargs='+', 
                       help='Custom list of endpoints to analyze (more efficient than broad discovery)')
    parser.add_argument('-f', '--endpoints-file', 
                       help='File containing list of endpoints (one per line)')
    parser.add_argument('-o', '--output', default='analysis.json', 
                       help='Output filename (default: analysis.json)')
    parser.add_argument('-t', '--timeout', type=int, default=10,
                       help='Request timeout in seconds (default: 10)')
    parser.add_argument('-d', '--delay', type=float, default=0.1,
                       help='Delay between requests in seconds (default: 0.1)')
    parser.add_argument('--swagger', action='store_true',
                       help='Generate Swagger specification from analysis')
    
    args = parser.parse_args()
    
    # Process custom endpoints
    custom_endpoints = None
    if args.endpoints:
        custom_endpoints = args.endpoints
        print(f"📋 Using custom endpoints: {custom_endpoints}")
    elif args.endpoints_file:
        try:
            with open(args.endpoints_file, 'r') as f:
                custom_endpoints = [line.strip() for line in f if line.strip()]
            print(f"📋 Loaded {len(custom_endpoints)} endpoints from {args.endpoints_file}")
        except FileNotFoundError:
            print(f"❌ Endpoints file not found: {args.endpoints_file}")
            return
        except Exception as e:
            print(f"❌ Error reading endpoints file: {e}")
            return
    
    # Create generator
    generator = UniversalAPIGenerator(
        base_url=args.base_url,
        custom_endpoints=custom_endpoints,
        timeout=args.timeout,
        delay=args.delay
    )
    
    # Generate analysis
    analysis = generator.generate_analysis()
    
    # Save to file
    generator.save_analysis(analysis, args.output)
    
    # Generate Swagger specification if requested
    if args.swagger:
        generator.generate_swagger_spec(args.output)
    
    # Print summary
    print("\n📊 Analysis Summary:")
    
    # Check if analysis was successful
    if analysis.get('status') == 'error':
        print(f"  ❌ Analysis failed: {analysis.get('message', 'Unknown error')}")
        return
    
    # Print metadata
    metadata = analysis.get('metadata', {})
    print(f"  Base URL: {metadata.get('base_url', 'Unknown')}")
    
    if custom_endpoints:
        print(f"  Custom Endpoints: {len(custom_endpoints)}")
    
    # Print summary statistics
    summary = analysis.get('summary', {})
    print(f"  Endpoints: {summary.get('total_endpoints', 0)}")
    
    if not custom_endpoints and 'discovery_rate' in summary:
        print(f"  Discovery Rate: {summary['discovery_rate']}")
    
    # Print CRUD operations
    crud_ops = summary.get('crud_operations', {})
    if crud_ops:
        print(f"  CRUD Operations:")
        for op, count in crud_ops.items():
            print(f"    {op.capitalize()}: {count}")
    
    # Print parameters and validation
    print(f"  Parameters: {summary.get('total_parameters', 0)}")
    validation_patterns = summary.get('validation_patterns', [])
    print(f"  Validation Patterns: {len(validation_patterns)}")


if __name__ == '__main__':
    main()
