#!/usr/bin/env python3
"""
Test script for HeroGateway Flask portal.

Usage:
    python test_portal.py

This script will:
1. Start the Flask app in a subprocess on port 5000
2. Run all acceptance tests
3. Report pass/fail for each test
4. Clean up any test data created
5. Stop the Flask app subprocess
"""

import json
import os
import re
import signal
import subprocess
import sys
import time

import requests


# Configuration
PORT = 5000
BASE_URL = f"http://127.0.0.1:{PORT}"
DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "keys.json")
ADMIN_USER = "admin"
ADMIN_PASS = "stone11031103"

# Colors for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"


def log_pass(msg):
    print(f"  {GREEN}PASS{RESET} {msg}")


def log_fail(msg):
    print(f"  {RED}FAIL{RESET} {msg}")


def start_app():
    """Start the Flask app in a subprocess and return the process handle."""
    env = os.environ.copy()
    env["ADMIN_USERNAME"] = ADMIN_USER
    env["ADMIN_PASSWORD"] = ADMIN_PASS
    env["FLASK_RUN_PORT"] = str(PORT)

    proc = subprocess.Popen(
        [sys.executable, "app.py"],
        cwd=os.path.dirname(__file__),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Wait for the server to become ready
    for _ in range(30):
        try:
            resp = requests.get(f"{BASE_URL}/login", timeout=1)
            if resp.status_code == 200:
                return proc
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(0.5)

    proc.terminate()
    proc.wait()
    raise RuntimeError("Flask app did not start within 15 seconds")


def stop_app(proc):
    """Gracefully stop the Flask app subprocess."""
    if proc.poll() is None:
        proc.send_signal(signal.SIGTERM)
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()


def load_data():
    """Load users from the JSON data file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            return json.loads(content) if content else []
    except (json.JSONDecodeError, IOError):
        return []


def save_data(users):
    """Save users to the JSON data file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)
        f.write("\n")


def cleanup_test_users():
    """Remove any users created by previous test runs."""
    users = load_data()
    cleaned = [u for u in users if not u.get("name", "").startswith("testuser_")]
    if len(cleaned) != len(users):
        save_data(cleaned)


class TestRunner:
    def __init__(self):
        self.session = requests.Session()
        self.passed = 0
        self.failed = 0
        self.test_users_created = []

    def check(self, condition, msg):
        if condition:
            log_pass(msg)
            self.passed += 1
        else:
            log_fail(msg)
            self.failed += 1

    def run_all(self):
        print("=" * 60)
        print("HeroGateway Portal Test Suite")
        print(f"Base URL: {BASE_URL}")
        print("=" * 60)

        self.test_login_page()
        self.test_login_failure()
        self.test_login_success()
        self.test_unauthenticated_blocked()
        self.test_user_creation_validation()
        self.test_user_creation_success()
        self.test_api_users_masked()
        self.test_data_persistence()

        print("=" * 60)
        print(f"Results: {GREEN}{self.passed} passed{RESET}, {RED}{self.failed} failed{RESET}")
        print("=" * 60)

        return self.failed == 0

    def test_login_page(self):
        print("\n[Login Page]")
        resp = self.session.get(f"{BASE_URL}/login")
        html = resp.text

        self.check(resp.status_code == 200, "Returns HTTP 200")
        self.check('<body class="signin">' in html, "Body has class 'signin'")
        self.check('<div class="signinpanel">' in html, "Form container has class 'signinpanel'")
        self.check("HeroGateway" in html, "Logo/name 'HeroGateway' present")
        self.check('name="username"' in html, "Username field present")
        self.check('name="password"' in html, "Password field present")
        self.check('type="submit"' in html, "Login button present")

    def test_login_failure(self):
        print("\n[Login Failure]")
        resp = self.session.post(
            f"{BASE_URL}/login",
            data={"username": "baduser", "password": "badpass"},
        )
        html = resp.text

        self.check(resp.status_code == 200, "Returns HTTP 200 (no redirect)")
        self.check("Invalid username or password" in html, "Error message displayed")

    def test_login_success(self):
        print("\n[Login Success]")
        resp = self.session.post(
            f"{BASE_URL}/login",
            data={"username": ADMIN_USER, "password": ADMIN_PASS},
            allow_redirects=True,
        )
        html = resp.text

        self.check(resp.status_code == 200, "Returns HTTP 200 after redirect")
        self.check("User Management" in html, "User Management page shown")
        self.check("Logout" in html, "Logout button present")

    def test_unauthenticated_blocked(self):
        print("\n[Unauthenticated Access]")
        # Use a fresh session with no cookies
        fresh = requests.Session()

        resp_users = fresh.get(f"{BASE_URL}/users", allow_redirects=False)
        self.check(
            resp_users.status_code in (302, 401),
            f"GET /users blocked (status {resp_users.status_code})",
        )

        resp_api = fresh.get(f"{BASE_URL}/api/users", allow_redirects=False)
        self.check(
            resp_api.status_code in (302, 401),
            f"GET /api/users blocked (status {resp_api.status_code})",
        )

        resp_post = fresh.post(
            f"{BASE_URL}/users", data={"username": "hacker"}, allow_redirects=False
        )
        self.check(
            resp_post.status_code in (302, 401),
            f"POST /users blocked (status {resp_post.status_code})",
        )

    def test_user_creation_validation(self):
        print("\n[User Creation Validation]")

        # Empty username
        resp = self.session.post(
            f"{BASE_URL}/users",
            data={"username": "", "display_name": ""},
            allow_redirects=False,
        )
        self.check(resp.status_code == 302, "Empty username returns redirect")
        resp2 = self.session.get(f"{BASE_URL}/users")
        self.check("Username is required" in resp2.text, "Empty username error shown")

        # Invalid characters
        resp = self.session.post(
            f"{BASE_URL}/users",
            data={"username": "bad name!", "display_name": ""},
            allow_redirects=False,
        )
        self.check(resp.status_code == 302, "Invalid username returns redirect")
        resp2 = self.session.get(f"{BASE_URL}/users")
        self.check(
            "Username may only contain" in resp2.text,
            "Invalid username error shown",
        )

        # Duplicate username (alice exists in seed data)
        resp = self.session.post(
            f"{BASE_URL}/users",
            data={"username": "alice", "display_name": ""},
            allow_redirects=False,
        )
        self.check(resp.status_code == 302, "Duplicate username returns redirect")
        resp2 = self.session.get(f"{BASE_URL}/users")
        self.check("Username already exists" in resp2.text, "Duplicate username error shown")

    def test_user_creation_success(self):
        print("\n[User Creation Success]")
        test_name = "testuser_" + str(int(time.time()))

        resp = self.session.post(
            f"{BASE_URL}/users",
            data={"username": test_name, "display_name": "Test Display Name"},
            allow_redirects=False,
        )
        self.check(resp.status_code == 302, "Creation returns redirect")

        # Fetch users page to verify key is shown
        resp2 = self.session.get(f"{BASE_URL}/users")
        html = resp2.text

        # Extract the API key from the success alert
        key_match = re.search(
            r'<code id="new-api-key"[^>]*>(hero_[A-Za-z0-9_\-]+)</code>', html
        )
        self.check(key_match is not None, "API key displayed after creation")

        if key_match:
            api_key = key_match.group(1)
            self.check(api_key.startswith("hero_"), "API key has 'hero_' prefix")
            self.check(len(api_key) > 20, f"API key is reasonably long ({len(api_key)} chars)")
            self.test_users_created.append(test_name)

        # Verify user appears in list
        self.check(test_name in html, "New user appears in list")

        # Verify masked key appears in the table
        masked_pattern = r"hero_[A-Za-z0-9_\-]{4}\*+"
        self.check(
            re.search(masked_pattern, html) is not None,
            "Masked API key shown in user list",
        )

    def test_api_users_masked(self):
        print("\n[API Users Endpoint]")
        resp = self.session.get(f"{BASE_URL}/api/users")
        self.check(resp.status_code == 200, "Returns HTTP 200")

        try:
            users = resp.json()
        except json.JSONDecodeError:
            log_fail("Response is valid JSON")
            self.failed += 1
            return

        self.check(isinstance(users, list), "Response is a JSON list")

        for user in users:
            key = user.get("api-key", "")
            # Keys should either be masked or short legacy keys fully masked
            if key.startswith("hero_") and "*" not in key:
                self.check(False, f"Full API key exposed for user '{user.get('name')}'")
                return

        self.check(True, "No full API keys exposed in API response")

    def test_data_persistence(self):
        print("\n[Data Persistence]")
        users = load_data()
        self.check(isinstance(users, list), "data/keys.json is a valid JSON list")

        for u in users:
            self.check("name" in u, f"User '{u.get('name')}' has 'name' field")
            self.check("api-key" in u, f"User '{u.get('name')}' has 'api-key' field")

        # Verify all test users we created are actually in the file
        for test_name in self.test_users_created:
            self.check(
                any(u.get("name") == test_name for u in users),
                f"Created user '{test_name}' persisted to JSON file",
            )


def main():
    proc = None

    try:
        print("Starting Flask app...")
        proc = start_app()
        print(f"Flask app started on port {PORT}")

        # Clean up any stale test users before running
        cleanup_test_users()

        runner = TestRunner()
        success = runner.run_all()

        # Clean up test users created during this run
        cleanup_test_users()

        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(130)
    finally:
        if proc is not None:
            print("\nStopping Flask app...")
            stop_app(proc)
            print("Flask app stopped")


if __name__ == "__main__":
    main()
