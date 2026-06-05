"""Tests for app.py main application."""
import subprocess
import sys


def test_app_imports():
    """Test that app.py can be imported directly."""
    code = """
import app as app_module
assert hasattr(app_module, 'app')
print('OK')
"""
    result = subprocess.run([sys.executable, '-c', code], capture_output=True, text=True, cwd='.')
    assert result.returncode == 0, f"Import failed: {result.stderr}"
    assert 'OK' in result.stdout


def test_index_route_redirects():
    """Test that the root route / redirects to /login."""
    code = """
import app as app_module

with app_module.app.test_client() as client:
    resp = client.get('/', follow_redirects=False)
    assert resp.status_code == 302
    assert '/login' in resp.headers.get('Location', '')
print('OK')
"""
    result = subprocess.run([sys.executable, '-c', code], capture_output=True, text=True, cwd='.')
    assert result.returncode == 0, f"Test failed: {result.stderr}"
    assert 'OK' in result.stdout
