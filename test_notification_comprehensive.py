#!/usr/bin/env python
"""
Comprehensive test of notification system
Kiểm tra toàn bộ hệ thống thông báo
"""
import requests
import json
from datetime import datetime

BASE_URL = 'http://localhost:8000'

def test_notification_system():
    print("=" * 60)
    print("NOTIFICATION SYSTEM TEST")
    print("=" * 60)
    
    # Test users
    test_users = [
        {'email': 'lecturer@edu.vn', 'password': 'lecturer123', 'role': 'Lecturer'},
        {'email': 'student@edu.vn', 'password': 'student123', 'role': 'Student'},
        {'email': 'hod@edu.vn', 'password': 'hod123', 'role': 'HOD'},
    ]
    
    for user in test_users:
        print(f"\n{'─' * 60}")
        print(f"Testing: {user['role']} ({user['email']})")
        print('─' * 60)
        
        try:
            # Login
            login_data = {'email': user['email'], 'password': user['password']}
            login_resp = requests.post(f'{BASE_URL}/auth/login', json=login_data, timeout=5)
            
            if login_resp.status_code != 200:
                print(f"❌ Login failed: {login_resp.status_code}")
                continue
            
            token = login_resp.json()['access_token']
            print("✓ Login successful")
            
            # Get notifications
            headers = {'Authorization': f'Bearer {token}'}
            notif_resp = requests.get(
                f'{BASE_URL}/notifications?skip=0&limit=50', 
                headers=headers, 
                timeout=5
            )
            
            if notif_resp.status_code != 200:
                print(f"❌ Failed to fetch notifications: {notif_resp.status_code}")
                print(f"   Response: {notif_resp.text[:200]}")
                continue
            
            data = notif_resp.json()
            total = data.get('total', 0)
            items = data.get('items', [])
            
            print(f"✓ Notifications fetched: {total} total")
            
            if items:
                unread = sum(1 for item in items if not item['is_read'])
                print(f"  • Unread: {unread}")
                print(f"  • Read: {total - unread}")
                print(f"\n  Notification list:")
                for item in items:
                    status = "✓" if item['is_read'] else "✗"
                    print(f"    [{status}] {item['title']}")
                    print(f"        Type: {item['notification_type']}, Date: {item['created_at'][:10]}")
            else:
                print("  (No notifications)")
            
            # Test filtering
            print(f"\n  Testing filters:")
            
            # Unread filter
            unread_resp = requests.get(
                f'{BASE_URL}/notifications?skip=0&limit=50&unread_only=true', 
                headers=headers, 
                timeout=5
            )
            if unread_resp.status_code == 200:
                unread_data = unread_resp.json()
                print(f"    • Unread only: {unread_data.get('total', 0)} notifications")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print(f"\n{'=' * 60}")
    print("TEST COMPLETED")
    print("=" * 60)

if __name__ == '__main__':
    test_notification_system()
