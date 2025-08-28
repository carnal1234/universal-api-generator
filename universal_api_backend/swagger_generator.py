#!/usr/bin/env python3
"""
Swagger Format Generator
Converts API analysis to Swagger/OpenAPI 3.0 format for use with swagger-ui-react
"""

import json
import time
from typing import Dict, List, Any, Optional
from pathlib import Path


class SwaggerGenerator:
    def __init__(self, analysis_file: str = "analysis.json"):
        """
        Initialize Swagger Generator
        
        Args:
            analysis_file: Path to analysis JSON file
        """
        self.analysis_file = analysis_file
        self.analysis = self._load_analysis()
        
    def _load_analysis(self) -> Dict[str, Any]:
        """Load analysis JSON file"""
        try:
            with open(self.analysis_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Analysis file not found: {self.analysis_file}")
            return {}
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON in analysis file: {self.analysis_file}")
            return {}
    
    def _convert_parameter_type(self, param_type: str) -> str:
        """Convert internal parameter type to OpenAPI type"""
        type_mapping = {
            'string': 'string',
            'integer': 'integer',
            'number': 'number',
            'boolean': 'boolean',
            'date': 'string',
            'email': 'string',
            'url': 'string',
            'uuid': 'string'
        }
        return type_mapping.get(param_type, 'string')
    
    def _create_parameter_schema(self, param_info: Dict) -> Dict:
        """Create OpenAPI parameter schema"""
        param_type = self._convert_parameter_type(param_info.get('type', 'string'))
        
        schema = {
            'type': param_type,
            'description': f"{param_info.get('name', 'parameter')} parameter"
        }
        
        # Add format for specific types
        if param_type == 'string':
            if param_info.get('type') == 'date':
                schema['format'] = 'date'
            elif param_info.get('type') == 'email':
                schema['format'] = 'email'
            elif param_info.get('type') == 'url':
                schema['format'] = 'uri'
            elif param_info.get('type') == 'uuid':
                schema['format'] = 'uuid'
        
        # Add default value if available
        if 'default' in param_info:
            schema['default'] = param_info['default']
        
        # Add example if available
        if 'example' in param_info:
            schema['example'] = param_info['example']
        
        return schema
    
    def _create_response_schema(self, response_schema: Dict) -> Dict:
        """Convert response schema to OpenAPI format"""
        if not response_schema:
            return {
                'type': 'object',
                'properties': {}
            }
        
        # Handle array responses
        if response_schema.get('type') == 'array':
            return {
                'type': 'array',
                'items': self._create_response_schema(response_schema.get('items', {}))
            }
        
        # Handle object responses
        if response_schema.get('type') == 'object':
            properties = {}
            for prop_name, prop_info in response_schema.get('properties', {}).items():
                properties[prop_name] = {
                    'type': self._convert_parameter_type(prop_info.get('type', 'string')),
                    'description': f"{prop_name} field"
                }
                
                # Add format for specific types
                if prop_info.get('type') == 'date':
                    properties[prop_name]['format'] = 'date'
                elif prop_info.get('type') == 'email':
                    properties[prop_name]['format'] = 'email'
                elif prop_info.get('type') == 'url':
                    properties[prop_name]['format'] = 'uri'
            
            return {
                'type': 'object',
                'properties': properties
            }
        
        # Default to object
        return {
            'type': 'object',
            'properties': {}
        }
    
    def _create_operation(self, endpoint: str, method: str, endpoint_data: Dict) -> Dict:
        """Create OpenAPI operation object"""
        method_lower = method.lower()
        method_params = endpoint_data.get('parameters', {}).get(method, {})
        response_schema = endpoint_data.get('response_schema', {}).get(method, {})
        parameter_validation = endpoint_data.get('parameter_validation', {}).get(method, {})
        
        operation = {
            'summary': f"{method} {endpoint}",
            'description': f"Endpoint for {endpoint}",
            'operationId': f"{method_lower}_{endpoint.replace('/', '_').replace('-', '_').strip('_')}",
            'tags': [endpoint.split('/')[1] if len(endpoint.split('/')) > 1 else 'default'],
            'responses': {
                '200': {
                    'description': 'Successful response',
                    'content': {
                        'application/json': {
                            'schema': self._create_response_schema(response_schema)
                        }
                    }
                },
                '400': {
                    'description': 'Bad request',
                    'content': {
                        'application/json': {
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'error': {'type': 'string'},
                                    'message': {'type': 'string'}
                                }
                            }
                        }
                    }
                },
                '404': {
                    'description': 'Not found',
                    'content': {
                        'application/json': {
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'error': {'type': 'string'},
                                    'message': {'type': 'string'}
                                }
                            }
                        }
                    }
                }
            }
        }
        
        # Add parameters only if they are actually accepted by this endpoint
        if method_params:
            operation['parameters'] = []
            for param_name, param_info in method_params.items():
                # Check if this parameter is actually accepted by this endpoint
                is_accepted = param_info.get('accepted', False)
                
                # Also check parameter validation to see if it has accepted values
                validation_info = parameter_validation.get(param_name, {})
                has_accepted_values = len(validation_info.get('accepted_values', [])) > 0
                
                # Only include parameter if it's accepted or has accepted values
                if is_accepted or has_accepted_values:
                    param_obj = {
                        'name': param_name,
                        'in': 'query',
                        'required': param_info.get('required', False),
                        'schema': self._create_parameter_schema(param_info)
                    }
                    
                    # Add description based on validation info
                    if validation_info.get('accepted_values'):
                        accepted_values = validation_info['accepted_values']
                        param_obj['schema']['description'] = f"{param_name} parameter. Accepted values: {', '.join(accepted_values[:3])}{'...' if len(accepted_values) > 3 else ''}"
                    
                    operation['parameters'].append(param_obj)
        
        # Add request body for POST/PUT/PATCH
        if method in ['POST', 'PUT', 'PATCH']:
            operation['requestBody'] = {
                'description': f'Data for {method} {endpoint}',
                'required': True,
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'data': {
                                    'type': 'object',
                                    'description': 'Request data'
                                }
                            }
                        }
                    }
                }
            }
        
        return operation
    
    def generate_swagger_spec(self) -> Dict[str, Any]:
        """Generate complete Swagger/OpenAPI 3.0 specification"""
        if not self.analysis:
            return {}
        
        metadata = self.analysis.get('metadata', {})
        endpoints = self.analysis.get('endpoints', {})
        
        # Create base OpenAPI spec
        swagger_spec = {
            'openapi': '3.0.0',
            'info': {
                'title': f"{metadata.get('generator', 'API')} Documentation",
                'description': f"API documentation generated by {metadata.get('generator', 'Universal API Generator')}",
                'version': metadata.get('version', '1.0.0'),
                # 'contact': {
                #     'name': 'API Support',
                #     'email': 'support@example.com'
                # }
            },
            'servers': [
                {
                    'url': metadata.get('base_url', 'https://api.example.com'),
                    'description': 'Production server'
                }
            ],
            'paths': {},
            'components': {
                'schemas': {},
                'parameters': {},
                'responses': {}
            },
            'tags': []
        }
        
        # Process each endpoint
        for endpoint, endpoint_data in endpoints.items():
            if endpoint_data.get('status') != 'success':
                continue
            
            methods = endpoint_data.get('methods', [])
            
            # Create path object
            path_obj = {}
            
            for method in methods:
                operation = self._create_operation(endpoint, method, endpoint_data)
                path_obj[method.lower()] = operation
            
            # Add path to spec
            swagger_spec['paths'][endpoint] = path_obj
            
            # Add tag
            tag_name = endpoint.split('/')[1] if len(endpoint.split('/')) > 1 else 'default'
            if tag_name not in [tag['name'] for tag in swagger_spec['tags']]:
                swagger_spec['tags'].append({
                    'name': tag_name,
                    'description': f'Operations for {tag_name}'
                })
        
        return swagger_spec
    
    def save_swagger_spec(self, output_file: str = "swagger.json") -> str:
        """Generate and save Swagger specification"""
        print("🔄 Generating Swagger specification...")
        
        swagger_spec = self.generate_swagger_spec()
        
        if not swagger_spec:
            print("❌ Failed to generate Swagger specification")
            return ""
        
        # Save to file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(swagger_spec, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Swagger specification saved to {output_file}")
        
        # Print summary
        paths_count = len(swagger_spec.get('paths', {}))
        operations_count = sum(len(path) for path in swagger_spec.get('paths', {}).values())
        tags_count = len(swagger_spec.get('tags', []))
        
        print(f"📊 Generated {paths_count} paths with {operations_count} operations")
        print(f"🏷️  {tags_count} tags created")
        
        return output_file


def main():
    """Main function for command line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate Swagger specification from API analysis')
    parser.add_argument('analysis_file', nargs='?', default='analysis.json',
                       help='Analysis JSON file (default: analysis.json)')
    parser.add_argument('-o', '--output', default='swagger.json',
                       help='Output filename (default: swagger.json)')
    
    args = parser.parse_args()
    
    # Generate Swagger spec
    generator = SwaggerGenerator(args.analysis_file)
    output_file = generator.save_swagger_spec(args.output)
    
    if output_file:
        print(f"\n🎉 Swagger specification ready!")
        print(f"📄 File: {output_file}")
        print(f"🌐 Use this file with swagger-ui-react in your React app")
    else:
        print(f"\n❌ Failed to generate Swagger specification")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
