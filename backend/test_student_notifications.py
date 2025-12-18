"""
Test notifications with student account
"""
import requests

BASE_URL = "http://127.0.0.1:8000"

def test_student_notifications():
    print("\n" + "="*60)
    print("  TESTING NOTIFICATIONS WITH STUDENT ACCOUNT")
    print("="*60 + "\n")
    
    # Login as student
    print("🔐 Logging in as student...")
    r = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": "student@test.com", "password": "student123"}
    )
    
    if r.status_code != 200:
        print(f"❌ Login failed: {r.text}")
        return
    
    token = r.json()["access_token"]
    print(f"✅ Student logged in")
    print(f"   Token: {token[:30]}...\n")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get all notifications
    print("📬 Getting notifications...")
    r = requests.get(f"{BASE_URL}/notifications/", headers=headers)
    
    if r.status_code == 200:
        data = r.json()
        print(f"✅ Total notifications: {data['total']}\n")
        
        if data['items']:
            for i, notif in enumerate(data['items'], 1):
                status = "📭 UNREAD" if not notif['is_read'] else "📬 READ"
                print(f"{status} #{i}: {notif['title']}")
                print(f"   Type: {notif['notification_type']}")
                print(f"   Message: {notif['message']}")
                print(f"   Created: {notif['created_at']}")
                print()
        else:
            print("   No notifications found")
    else:
        print(f"❌ Failed: {r.text}")
    
    # Check if following syllabus
    print("👥 Checking follow status...")
    r = requests.get(f"{BASE_URL}/notifications/following/151", headers=headers)
    
    if r.status_code == 200:
        data = r.json()
        print(f"✅ Following status: {data['is_following']}")
        if data['is_following']:
            print(f"   Followed at: {data['followed_at']}")
    else:
        print(f"❌ Failed: {r.text}")
    
    print("\n" + "="*60)
    print("✅ STUDENT NOTIFICATION TEST COMPLETED")
    print("="*60 + "\n")

if __name__ == "__main__":
    test_student_notifications()
