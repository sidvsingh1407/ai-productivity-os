import pytest
import os
import subprocess
import sys

def test_script_fences_production():
    # Make sure we're in backend dir
    env = os.environ.copy()
    env["ENVIRONMENT"] = "production"

    scripts = ["audit_script.py", "check_scores.py", "seed_db.py"]
    for script in scripts:
        result = subprocess.run([sys.executable, script], env=env, capture_output=True, text=True)
        assert result.returncode == 1, f"{script} did not exit with code 1 in production"
        assert "Cannot run data mutation/schema creation script in production" in result.stdout

def test_script_fences_non_production_missing_flag():
    env = os.environ.copy()
    env["ENVIRONMENT"] = "development"

    scripts = ["audit_script.py", "check_scores.py", "seed_db.py"]
    for script in scripts:
        result = subprocess.run([sys.executable, script], env=env, capture_output=True, text=True)
        assert result.returncode == 1, f"{script} did not exit with code 1 when missing explicit opt-in"
        assert "Explicit opt-in required" in result.stdout

def test_script_fences_non_production_with_flag():
    env = os.environ.copy()
    env["ENVIRONMENT"] = "development"
    env["I_KNOW_WHAT_I_AM_DOING"] = "true"

    # We will just test seed_db.py which runs and might fail or succeed on local test db
    # We just want to ensure it doesn't immediately exit with the fencing print.
    result = subprocess.run([sys.executable, "seed_db.py"], env=env, capture_output=True, text=True)
    assert "Cannot run data mutation/schema creation script" not in result.stdout
    assert "Explicit opt-in required" not in result.stdout
