#!/usr/bin/env python
"""Test notification API endpoint"""
import requests
import json

try:
    # Login
    login_data = {'email': 'lecturer@edu.vn', 'password': 'lecturer123'}
    login_resp = requests.post('http://localhost:8000/auth/login', json=login_data)
    if login_resp.status_code != 200:
        print(f'Login failed: {login_resp.status_code}')
        exit(1)
    
    token = login_resp.json()['access_token']
    print('✓ Logged in successfully')
    
    # Get notifications
    headers = {'Authorization': f'Bearer {token}'}
    notif_resp = requests.get('http://localhost:8000/notifications?skip=0&limit=50', headers=headers)
    
    if notif_resp.status_code != 200:
        print(f'Failed to fetch notifications: {notif_resp.status_code}')
        print(notif_resp.text)
        exit(1)
    
    notif_data = notif_resp.json()
    
    print(f'✓ Fetched notifications')
    print(f'\nTotal notifications: {notif_data.get("total", 0)}')
    
    if notif_data.get('items'):
        for item in notif_data['items']:
            read_status = '✓ Read' if item.get('is_read') else '✗ Unread'
            print(f'  - [{read_status}] {item["title"]} ({item["notification_type"]})')
    else:
        print('  No notifications found')
        
except Exception as e:
    print(f'Error: {e}')
