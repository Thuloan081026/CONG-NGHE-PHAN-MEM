import requests

# Get index.html from server
response = requests.get('http://localhost:3000/index.html')
content = response.text

# Check if debug logging exists
if "console.log('User role type:" in content:
    print("✅ index.html contains new debug logging")
else:
    print("❌ index.html does NOT contain new debug logging")

# Show actual content around redirectToDashboard
if 'redirectToDashboard' in content:
    start = content.find('function redirectToDashboard')
    end = content.find('function showAlert', start)
    snippet = content[start:end]
    
    print("\nRelevant code:")
    print("=" * 60)
    for i, line in enumerate(snippet.split('\n')[:15]):
        print(f"{i:2d}: {line}")
