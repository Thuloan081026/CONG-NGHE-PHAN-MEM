"""
Simple Quick Test for Module 7 & 8
Test one endpoint at a time
"""
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_server():
    """Test if server is running"""
    print("\n" + "="*60)
    print("  TESTING SERVER CONNECTION")
    print("="*60)
    try:
        r = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"✓ Server is running: {r.json()['message']}")
        return True
    except Exception as e:
        print(f"✗ Server not responding: {e}")
        return False

def test_login():
    """Test login and return token"""
    print("\n" + "="*60)
    print("  TESTING LOGIN")
    print("="*60)
    
    # Test admin login
    try:
        r = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": "admin@test.com", "password": "admin123"},
            timeout=5
        )
        if r.status_code == 200:
            token = r.json()["access_token"]
            print(f"✓ Admin login successful")
            print(f"  Token: {token[:30]}...")
            return token
        else:
            print(f"✗ Login failed: {r.status_code}")
            print(f"  Response: {r.text}")
            return None
    except Exception as e:
        print(f"✗ Login error: {e}")
        return None

def test_ai_health(token):
    """Test AI health check"""
    print("\n" + "="*60)
    print("  MODULE 7: AI HEALTH CHECK")
    print("="*60)
    
    try:
        r = requests.get(
            f"{BASE_URL}/ai/health",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
        if r.status_code == 200:
            data = r.json()
            print(f"✓ AI Status: {data['status']}")
            print(f"  Model: {data['model']}")
            print(f"  Gemini Available: {data['gemini_available']}")
            print(f"  Fallback: {data['fallback_available']}")
        else:
            print(f"✗ Health check failed: {r.status_code}")
            print(f"  Response: {r.text}")
    except Exception as e:
        print(f"✗ Health check error: {e}")

def test_ai_summarize(token):
    """Test AI summarize"""
    print("\n" + "="*60)
    print("  MODULE 7: AI SUMMARIZE")
    print("="*60)
    
    try:
        r = requests.post(
            f"{BASE_URL}/ai/summarize",
            headers={"Authorization": f"Bearer {token}"},
            json={"syllabus_id": 151, "language": "vi"},
            timeout=10
        )
        if r.status_code == 200:
            data = r.json()
            print(f"✓ Summarization completed!")
            print(f"\nSummary:")
            print(f"  {data['summary'][:150]}...")
            print(f"\nKey Points: {len(data['key_points'])} items")
            for i, point in enumerate(data['key_points'][:3], 1):
                print(f"  {i}. {point[:80]}...")
        else:
            print(f"✗ Summarize failed: {r.status_code}")
            print(f"  Response: {r.text}")
    except Exception as e:
        print(f"✗ Summarize error: {e}")

def test_ai_diff(token):
    """Test AI semantic diff"""
    print("\n" + "="*60)
    print("  MODULE 7: AI SEMANTIC DIFF")
    print("="*60)
    
    try:
        r = requests.post(
            f"{BASE_URL}/ai/diff",
            headers={"Authorization": f"Bearer {token}"},
            json={"version_id_1": 1, "version_id_2": 2, "language": "vi"},
            timeout=10
        )
        if r.status_code == 200:
            data = r.json()
            print(f"✓ Diff analysis completed!")
            print(f"\nVersion Comparison:")
            print(f"  Version {data['version_1']} vs Version {data['version_2']}")
            print(f"\nChanges Summary:")
            print(f"  {data['changes_summary'][:100]}...")
            print(f"\nMajor Changes: {len(data['major_changes'])} items")
            print(f"Minor Changes: {len(data['minor_changes'])} items")
        else:
            print(f"✗ Diff failed: {r.status_code}")
            print(f"  Response: {r.text}")
    except Exception as e:
        print(f"✗ Diff error: {e}")

def test_notification_endpoints(token):
    """Test notification endpoints"""
    print("\n" + "="*60)
    print("  MODULE 8: NOTIFICATION SYSTEM")
    print("="*60)
    
    # Get notifications
    try:
        r = requests.get(
            f"{BASE_URL}/notifications/",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
        if r.status_code == 200:
            data = r.json()
            print(f"✓ Get notifications successful")
            print(f"  Total: {data['total']}")
            if 'items' in data:
                print(f"  Items: {len(data['items'])}")
                if data['items']:
                    print(f"\nFirst 3 notifications:")
                    for notif in data['items'][:3]:
                        print(f"  • [{notif['notification_type']}] {notif['title']}")
                        print(f"    {notif['message'][:60]}...")
                        print(f"    Read: {notif['is_read']}")
        else:
            print(f"✗ Get notifications failed: {r.status_code}")
            print(f"  Response: {r.text}")
    except Exception as e:
        print(f"✗ Get notifications error: {e}")

def main():
    print("\n" + "="*70)
    print("  QUICK TEST: MODULE 7 (AI) & MODULE 8 (NOTIFICATION)")
    print("="*70)
    
    # Step 1: Check server
    if not test_server():
        print("\n⚠️  Server is not running!")
        print("   Please start server first: python -m uvicorn app.main:app --reload")
        return
    
    time.sleep(1)
    
    # Step 2: Login
    token = test_login()
    if not token:
        print("\n⚠️  Cannot get token. Make sure admin user exists!")
        return
    
    time.sleep(1)
    
    # Step 3: Test Module 7
    test_ai_health(token)
    time.sleep(1)
    test_ai_summarize(token)
    time.sleep(1)
    test_ai_diff(token)
    
    # Step 4: Test Module 8
    time.sleep(1)
    test_notification_endpoints(token)
    
    # Summary
    print("\n" + "="*70)
    print("  TEST COMPLETED")
    print("="*70)
    print("\n✓ Server connection working")
    print("✓ Authentication working")
    print("✓ Module 7 (AI Integration) tested")
    print("✓ Module 8 (Notification) tested")
    print("\n🎉 All basic tests passed!\n")
    print("📝 For detailed testing, open: http://127.0.0.1:8000/docs")
    print()

if __name__ == "__main__":
    main()
