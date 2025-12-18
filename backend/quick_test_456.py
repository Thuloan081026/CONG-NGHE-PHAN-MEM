"""Quick test - Test modules 4, 5, 6 (already passing)"""
import subprocess
import sys

print("Testing modules 4-6 (Review, CLO-PLO, Search)...")
cmd = ["python", "-m", "pytest", 
       "tests/test_review.py", 
       "tests/test_clo_plo.py", 
       "tests/test_search.py",
       "-v", "--tb=no", "-q"]
result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
print(result.stdout)
print(result.stderr)
sys.exit(result.returncode)
