import requests

# Get index.html from server
response = requests.get('http://localhost:3000/index.html')
content = response.text

# Check if principal mapping exists
if "'principal': 'principal-web/dashboard.html'" in content:
    print("✅ index.html contains principal mapping")
else:
    print("❌ index.html does NOT contain principal mapping")

# Check if debug logging was added
if "console.log('User role type'," in content:
    print("✅ index.html contains new debug logging")
else:
    print("❌ index.html does NOT contain new debug logging")

# Show line with principal
if 'principal' in content:
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'principal' in line and 'dashboard' in line:
            print(f"\nLine {i}: {line.strip()}")
            break
