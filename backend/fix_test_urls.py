"""
Script để fix tất cả API URLs trong test files
Thay /api/v1/ thành /
"""
import re
import os

# Test files cần fix
files = [
    "tests/test_auth.py",
    "tests/test_syllabus.py",
    "tests/test_workflow.py"
]

for file_path in files:
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        continue
    
    print(f"🔧 Fixing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Thay thế /api/v1/xxx thành /xxx
    new_content = content.replace('"/api/v1/', '"/')
    
    # Ghi lại file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Fixed {file_path}")

print("\n✅ Done! All test files have been updated.")
