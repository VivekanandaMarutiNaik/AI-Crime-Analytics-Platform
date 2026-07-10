from pathlib import Path
import subprocess
import sys

BASE_DIR = Path(__file__).resolve().parent

validators = [
    "validate_primary_keys.py",
    "validate_foreign_keys.py",
    "validate_dates.py",
    "validate_relationships.py",
]

print("=" * 60)
print(" AI Crime Analytics Platform - Database Validation")
print("=" * 60)

all_passed = True

for validator in validators:
    print(f"\nRunning {validator}...\n")

    result = subprocess.run(
        [sys.executable, str(BASE_DIR / validator)]
    )

    if result.returncode != 0:
        all_passed = False
        print(f"\n❌ {validator} FAILED\n")
    else:
        print(f"\n✅ {validator} COMPLETED\n")

print("=" * 60)

if all_passed:
    print("🎉 ALL VALIDATIONS COMPLETED SUCCESSFULLY")
else:
    print("⚠️ Some validators failed.")

print("=" * 60)