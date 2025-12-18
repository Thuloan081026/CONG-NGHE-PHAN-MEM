"""
Test Gemini AI Integration
"""
import sys
import os

# Test import
try:
    import google.generativeai as genai
    print("✅ google-generativeai installed")
except ImportError:
    print("❌ google-generativeai NOT installed")
    print("Run: pip install google-generativeai")
    sys.exit(1)

# Test configuration
try:
    # This will use the key from config.py
    from app.core.config import settings
    print(f"✅ Config loaded")
    print(f"   API Key: {settings.GEMINI_API_KEY[:20]}..." if len(settings.GEMINI_API_KEY) > 20 else "   API Key: NOT SET")
    print(f"   Model: {settings.GEMINI_MODEL}")
    
    # Try to configure Gemini
    if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE":
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel(settings.GEMINI_MODEL)
        
        # Test simple prompt
        print("\n🤖 Testing Gemini AI...")
        response = model.generate_content("Say 'Hello from Gemini!' in Vietnamese")
        print(f"✅ Gemini response: {response.text}")
        print("\n🎉 GEMINI AI WORKING!")
    else:
        print("\n⚠️  API Key chưa được set!")
        print("   Hướng dẫn:")
        print("   1. Truy cập: https://makersuite.google.com/app/apikey")
        print("   2. Tạo API key (miễn phí)")
        print("   3. Sửa app/core/config.py: GEMINI_API_KEY = 'your-key-here'")
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nCách fix:")
    print("1. Lấy API key: https://makersuite.google.com/app/apikey")
    print("2. Update app/core/config.py")
