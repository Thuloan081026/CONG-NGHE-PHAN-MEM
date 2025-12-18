#!/usr/bin/env python3
"""
Simple Flask server for testing - minimal version
"""

from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Test Server</title>
</head>
<body>
    <h1>Flask Server is Working!</h1>
    <p>If you can see this, the server is running correctly.</p>
    <p>Time: <span id="time"></span></p>

    <script>
        document.getElementById('time').textContent = new Date().toLocaleString();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    print("🚀 Starting simple test server...")
    print("🌐 URL: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)