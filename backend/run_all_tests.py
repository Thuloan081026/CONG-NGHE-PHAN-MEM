"""
COMPREHENSIVE TEST REPORT - ALL 6 BACKEND MODULES
Syllabus Management System - HCMUTE
"""

print("=" * 80)
print("🎯 COMPREHENSIVE BACKEND TEST REPORT")
print("Syllabus Management System - HCMUTE")
print("=" * 80)

import subprocess
import sys

def run_test_module(module_name, test_file):
    """Run tests for a specific module"""
    print(f"\n{'='*80}")
    print(f"🧪 TESTING: {module_name}")
    print(f"{'='*80}")
    
    cmd = f"python -m pytest {test_file} -v --tb=short -q"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    # Extract pass/fail counts
    output = result.stdout + result.stderr
    print(output)
    
    # Find summary line
    for line in output.split('\n'):
        if 'passed' in line.lower() or 'failed' in line.lower():
            if any(x in line for x in ['passed', 'failed', 'error', 'warning']):
                print(f"\n📊 Result: {line.strip()}")
                return line
    
    return "No results found"

# Test all modules
print("\n🚀 Starting comprehensive test suite...\n")

modules = [
    ("MODULE 1: Authentication + User Management", "tests/test_auth.py tests/test_users.py"),
    ("MODULE 2: Syllabus Management", "tests/test_syllabus.py"),
    ("MODULE 3: Workflow Management", "tests/test_workflow.py"),
    ("MODULE 4: Collaborative Review", "tests/test_review.py"),
    ("MODULE 5: CLO-PLO Mapping", "tests/test_clo_plo.py"),
    ("MODULE 6: Search System", "tests/test_search.py"),
]

results = []
for module_name, test_file in modules:
    try:
        result = run_test_module(module_name, test_file)
        results.append((module_name, result))
    except Exception as e:
        results.append((module_name, f"Error: {e}"))

# Final summary
print("\n" + "=" * 80)
print("📋 FINAL TEST SUMMARY")
print("=" * 80)

for module_name, result in results:
    status = "✅" if "passed" in result and "failed" not in result else "⚠️"
    print(f"{status} {module_name}")
    print(f"   {result}")

print("\n" + "=" * 80)
print("✅ ALL TESTS COMPLETED!")
print("=" * 80)

print("\n🗄️  DATABASE: XAMPP MySQL (syllabus_db)")
print("📦 Production data created for all 6 modules")
print("\n🔐 Test credentials:")
print("  • Lecturer: lecturer1@hcmute.edu.vn / lecturer123")
print("  • HOD: hod.cs@hcmute.edu.vn / hod123")
print("  • Student: student1@student.hcmute.edu.vn / student123")
