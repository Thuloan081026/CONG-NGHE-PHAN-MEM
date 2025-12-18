import sys
sys.path.insert(0, '.')
from tests.test_clo_plo import client, auth_header, setup_test_data, test_clo, test_plo_id, lecturer_token

# Setup
setup_test_data()

# Test create mapping
data = {
    'clo_id': test_clo['id'],
    'plo_id': test_plo_id,
    'correlation_level': 'high',
    'correlation_score': 0.8,
    'notes': 'Strong correlation'
}

response = client.post('/clo-plo/mapping', json=data, headers=auth_header(lecturer_token))
print(f'Status: {response.status_code}')
print(f'Content-Type: {response.headers.get("content-type")}')
print(f'Response text: {response.text[:1000]}')
try:
    json_data = response.json()
    print(f'JSON: {json_data}')
except Exception as e:
    print(f'JSON Error: {e}')
