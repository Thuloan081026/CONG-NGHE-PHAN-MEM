#!/usr/bin/env python3
"""
Test API endpoints
"""

import requests
import json

def test_api():
    print('🧪 Testing API Endpoints...')
    print('=' * 50)

    base_url = 'http://127.0.0.1:8000'

    # Test health check
    try:
        response = requests.get(f'{base_url}/')
        print(f'✅ Health Check: {response.status_code}')
        print(f'   Response: {response.json()}')
    except Exception as e:
        print(f'❌ Health Check failed: {e}')

    print()

    # Test test endpoint
    try:
        response = requests.get(f'{base_url}/test')
        print(f'✅ Test Endpoint: {response.status_code}')
        print(f'   Response: {response.json()}')
    except Exception as e:
        print(f'❌ Test Endpoint failed: {e}')

    print()
    print('🎉 API Testing completed!')

if __name__ == '__main__':
    test_api()