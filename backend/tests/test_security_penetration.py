"""
Security Penetration Testing Suite

This module contains penetration testing scripts to identify security vulnerabilities
in the authentication system. These tests simulate real-world attack scenarios.

⚠️ WARNING: These tests should only be run in controlled test environments.
Do not run against production systems without authorization.

Test Plan Reference: AUTH_TEST_PLAN.md
Security Assessment: SECURITY_VULNERABILITIES.md

Coverage:
- Brute Force Attacks
- Token Manipulation
- Session Hijacking
- Injection Attacks
- Authentication Bypass Attempts
- Privilege Escalation
"""

import pytest
import jwt
import time
import hashlib
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from main import app
from auth import SECRET_KEY, ALGORITHM
import concurrent.futures

client = TestClient(app)


class TestBruteForceAttacks:
    """Simulate brute force attack scenarios"""
    
    def test_password_brute_force_attempt(self):
        """
        Simulate brute force password guessing attack
        
        Tests vulnerability: VULN-HIGH-001 (No Rate Limiting)
        """
        # Register a test user
        test_user = {
            "email": "bruteforce@example.com",
            "password": "SecurePass123!",
            "full_name": "Brute Force Test"
        }
        client.post("/api/auth/register", json=test_user)
        
        # Common passwords to try
        common_passwords = [
            "password", "123456", "12345678", "qwerty",
            "abc123", "monkey", "1234567", "letmein",
            "trustno1", "dragon"
        ]
        
        successful_attempts = 0
        failed_attempts = 0
        rate_limited = False
        
        # Attempt multiple logins
        for password in common_passwords:
            response = client.post("/api/auth/login", json={
                "email": test_user["email"],
                "password": password
            })
            
            if response.status_code == 200:
                successful_attempts += 1
            elif response.status_code == 429:  # Rate limited
                rate_limited = True
                break
            else:
                failed_attempts += 1
        
        # Analysis
        print(f"\n[BRUTE FORCE TEST]")
        print(f"Attempts: {failed_attempts + successful_attempts}")
        print(f"Failed: {failed_attempts}")
        print(f"Successful: {successful_attempts}")
        print(f"Rate Limited: {rate_limited}")
        
        # Vulnerability Assessment
        if not rate_limited and failed_attempts > 5:
            print("⚠️  VULNERABILITY: No rate limiting detected!")
            print("   Recommendation: Implement rate limiting (VULN-HIGH-001)")
        else:
            print("✓  Rate limiting appears to be working")
    
    def test_concurrent_login_attempts(self):
        """
        Simulate distributed brute force attack with concurrent requests
        
        Tests: Rate limiting under concurrent load
        """
        test_user = {
            "email": "concurrent@example.com",
            "password": "SecurePass123!",
            "full_name": "Concurrent Test"
        }
        client.post("/api/auth/register", json=test_user)
        
        def attempt_login(password):
            """Single login attempt"""
            try:
                response = client.post("/api/auth/login", json={
                    "email": test_user["email"],
                    "password": password
                }, timeout=5)
                return response.status_code
            except:
                return 500
        
        # Generate password attempts
        passwords = [f"password{i}" for i in range(20)]
        
        # Execute concurrent requests
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(attempt_login, passwords))
        end_time = time.time()
        
        # Analysis
        rate_limited_count = results.count(429)
        failed_count = results.count(401)
        
        print(f"\n[CONCURRENT ATTACK TEST]")
        print(f"Total Requests: {len(results)}")
        print(f"Duration: {end_time - start_time:.2f}s")
        print(f"Rate Limited: {rate_limited_count}")
        print(f"Failed: {failed_count}")
        
        if rate_limited_count == 0:
            print("⚠️  VULNERABILITY: No rate limiting under concurrent load!")
        else:
            print(f"✓  Rate limiting active ({rate_limited_count}/{len(results)} blocked)")


class TestTokenManipulation:
    """Test JWT token security and manipulation attempts"""
    
    @pytest.fixture
    def valid_token(self):
        """Get a valid token for testing"""
        user = {
            "email": "tokentest@example.com",
            "password": "SecurePass123!",
            "full_name": "Token Test"
        }
        client.post("/api/auth/register", json=user)
        response = client.post("/api/auth/login", json={
            "email": user["email"],
            "password": user["password"]
        })
        return response.json()["access_token"]
    
    def test_token_signature_tampering(self, valid_token):
        """
        Attempt to tamper with token signature
        
        Tests: TC-SEC-030 (Token Tampering)
        """
        # Decode token
        payload = jwt.decode(
            valid_token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_signature": False}
        )
        
        print(f"\n[TOKEN TAMPERING TEST]")
        print(f"Original Payload: {payload}")
        
        # Attempt 1: Change role to admin
        tampered_payload = payload.copy()
        tampered_payload["role"] = "admin"
        
        # Try different secrets
        test_secrets = [
            "wrong-secret",
            "",
            "secret",
            "SECRET_KEY",
            SECRET_KEY[::-1],  # Reversed
        ]
        
        vulnerabilities_found = 0
        
        for secret in test_secrets:
            try:
                tampered_token = jwt.encode(tampered_payload, secret, algorithm=ALGORITHM)
                
                # Try to access admin endpoint
                response = client.get(
                    "/api/admin/users",
                    headers={"Authorization": f"Bearer {tampered_token}"}
                )
                
                if response.status_code == 200:
                    print(f"⚠️  CRITICAL: Token accepted with wrong secret: {secret}")
                    vulnerabilities_found += 1
                    
            except Exception as e:
                pass
        
        if vulnerabilities_found == 0:
            print("✓  Token signature validation working correctly")
        else:
            print(f"⚠️  CRITICAL: {vulnerabilities_found} signature bypass(es) found!")
    
    def test_token_expiry_manipulation(self, valid_token):
        """
        Attempt to extend token expiry time
        
        Tests: Token expiration enforcement
        """
        # Decode token
        payload = jwt.decode(
            valid_token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_signature": False}
        )
        
        print(f"\n[TOKEN EXPIRY MANIPULATION TEST]")
        
        # Attempt to extend expiry
        extended_payload = payload.copy()
        extended_payload["exp"] = datetime.utcnow() + timedelta(days=365)
        
        # Re-encode with wrong secret (should fail)
        try:
            extended_token = jwt.encode(extended_payload, "wrong-secret", algorithm=ALGORITHM)
            
            response = client.get(
                "/api/bookings",
                headers={"Authorization": f"Bearer {extended_token}"}
            )
            
            if response.status_code == 200:
                print("⚠️  CRITICAL: Extended token accepted!")
            else:
                print("✓  Extended token rejected")
                
        except Exception as e:
            print(f"✓  Token manipulation prevented: {type(e).__name__}")
    
    def test_algorithm_confusion_attack(self, valid_token):
        """
        Attempt algorithm confusion attack (HS256 vs RS256)
        
        Tests: Algorithm verification
        """
        print(f"\n[ALGORITHM CONFUSION TEST]")
        
        # Decode token
        payload = jwt.decode(
            valid_token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_signature": False}
        )
        
        # Try different algorithms
        test_algorithms = ["HS512", "RS256", "none"]
        
        for alg in test_algorithms:
            try:
                if alg == "none":
                    # None algorithm attack
                    confused_token = jwt.encode(payload, "", algorithm="none")
                else:
                    confused_token = jwt.encode(payload, SECRET_KEY, algorithm=alg)
                
                response = client.get(
                    "/api/bookings",
                    headers={"Authorization": f"Bearer {confused_token}"}
                )
                
                if response.status_code == 200:
                    print(f"⚠️  VULNERABILITY: Token with {alg} algorithm accepted!")
                else:
                    print(f"✓  Token with {alg} algorithm rejected")
                    
            except Exception as e:
                print(f"✓  {alg} algorithm prevented: {type(e).__name__}")


class TestInjectionAttacks:
    """Test injection attack prevention"""
    
    @pytest.mark.parametrize("injection_payload", [
        # SQL Injection
        "admin' OR '1'='1",
        "admin'--",
        "admin' OR 1=1--",
        "'; DROP TABLE users;--",
        "' UNION SELECT * FROM users--",
        "admin' AND '1'='1",
        
        # NoSQL Injection
        '{"$gt": ""}',
        '{"$ne": null}',
        '{"$regex": ".*"}',
        
        # Command Injection
        "; ls -la",
        "| cat /etc/passwd",
        "&& whoami",
    ])
    def test_injection_in_login(self, injection_payload):
        """
        Test various injection attacks in login endpoint
        
        Tests: TC-SEC-001, TC-SEC-002 (SQL Injection Prevention)
        """
        response = client.post("/api/auth/login", json={
            "email": injection_payload,
            "password": injection_payload
        })
        
        # Should not execute injection
        assert response.status_code in [401, 422]
        
        # Check response doesn't leak information
        detail = response.json().get("detail", "").lower()
        sensitive_keywords = ["sql", "database", "table", "query", "syntax", "error"]
        
        for keyword in sensitive_keywords:
            if keyword in detail:
                print(f"⚠️  Information Leakage: '{keyword}' in error message")
                print(f"   Detail: {detail}")


class TestAuthenticationBypass:
    """Test authentication bypass attempts"""
    
    def test_direct_admin_access_without_auth(self):
        """
        Attempt to access admin endpoints without authentication
        
        Tests: TC-AUTH-032 (Unauthenticated Access)
        """
        admin_endpoints = [
            "/api/admin/users",
            "/api/admin/bookings",
            "/api/admin/stats"
        ]
        
        print(f"\n[AUTHENTICATION BYPASS TEST]")
        
        bypassed = []
        for endpoint in admin_endpoints:
            response = client.get(endpoint)
            
            if response.status_code == 200:
                print(f"⚠️  CRITICAL: {endpoint} accessible without auth!")
                bypassed.append(endpoint)
            else:
                print(f"✓  {endpoint} protected (status: {response.status_code})")
        
        assert len(bypassed) == 0, f"Endpoints bypassed: {bypassed}"
    
    def test_privilege_escalation_attempt(self):
        """
        Attempt to escalate privileges from user to admin
        
        Tests: TC-AUTH-031 (User Access to Admin Endpoints)
        """
        # Register regular user
        user = {
            "email": "escalation@example.com",
            "password": "SecurePass123!",
            "full_name": "Escalation Test"
        }
        client.post("/api/auth/register", json=user)
        
        # Login as regular user
        response = client.post("/api/auth/login", json={
            "email": user["email"],
            "password": user["password"]
        })
        user_token = response.json()["access_token"]
        
        # Attempt to access admin endpoints
        response = client.get(
            "/api/admin/users",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        
        print(f"\n[PRIVILEGE ESCALATION TEST]")
        if response.status_code == 200:
            print("⚠️  CRITICAL: Regular user accessed admin endpoint!")
        elif response.status_code == 403:
            print("✓  Privilege escalation prevented (403 Forbidden)")
        else:
            print(f"✓  Access denied (status: {response.status_code})")
        
        assert response.status_code != 200


class TestSessionSecurity:
    """Test session management security"""
    
    def test_token_reuse_after_logout(self):
        """
        Test if tokens can be reused after logout
        
        Tests: VULN-HIGH-002 (No JWT Token Blacklist)
        """
        # Register and login
        user = {
            "email": "logout@example.com",
            "password": "SecurePass123!",
            "full_name": "Logout Test"
        }
        client.post("/api/auth/register", json=user)
        
        response = client.post("/api/auth/login", json={
            "email": user["email"],
            "password": user["password"]
        })
        token = response.json()["access_token"]
        
        # Use token (should work)
        response = client.get(
            "/api/bookings",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code != 401
        
        # Logout (if endpoint exists)
        logout_response = client.post(
            "/api/auth/logout",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print(f"\n[TOKEN REUSE TEST]")
        
        if logout_response.status_code == 404:
            print("⚠️  WARNING: No logout endpoint implemented")
            print("   Vulnerability: VULN-HIGH-002 (No Token Blacklist)")
            return
        
        # Try to reuse token after logout
        response = client.get(
            "/api/bookings",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            print("⚠️  VULNERABILITY: Token still valid after logout!")
            print("   Recommendation: Implement token blacklist")
        else:
            print("✓  Token invalidated after logout")


class TestInformationDisclosure:
    """Test for information disclosure vulnerabilities"""
    
    def test_user_enumeration_via_timing(self):
        """
        Test if user enumeration is possible via response timing
        
        Tests: VULN-LOW-007 (Account Enumeration Protection)
        """
        # Test with existing user
        existing_user = {
            "email": "existing@example.com",
            "password": "SecurePass123!",
            "full_name": "Existing User"
        }
        client.post("/api/auth/register", json=existing_user)
        
        # Measure response time for existing user
        start = time.time()
        response1 = client.post("/api/auth/login", json={
            "email": existing_user["email"],
            "password": "wrongpassword"
        })
        time_existing = time.time() - start
        
        # Measure response time for non-existent user
        start = time.time()
        response2 = client.post("/api/auth/login", json={
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        })
        time_nonexistent = time.time() - start
        
        print(f"\n[USER ENUMERATION TEST]")
        print(f"Existing user response time: {time_existing:.4f}s")
        print(f"Non-existent user response time: {time_nonexistent:.4f}s")
        print(f"Time difference: {abs(time_existing - time_nonexistent):.4f}s")
        
        # Check if timing difference is significant
        if abs(time_existing - time_nonexistent) > 0.1:
            print("⚠️  WARNING: Timing difference may allow user enumeration")
        else:
            print("✓  Response times are similar")
        
        # Check if error messages are the same
        if response1.json()["detail"] == response2.json()["detail"]:
            print("✓  Error messages are identical")
        else:
            print("⚠️  WARNING: Different error messages may reveal user existence")
    
    def test_password_in_error_messages(self):
        """
        Test if passwords appear in error messages or logs
        
        Tests: TC-SEC-041 (Password in Response)
        """
        test_password = "TestPassword123!"
        
        # Attempt registration with various invalid inputs
        response = client.post("/api/auth/register", json={
            "email": "invalid-email",
            "password": test_password,
            "full_name": "Test"
        })
        
        print(f"\n[PASSWORD DISCLOSURE TEST]")
        
        if test_password in response.text:
            print("⚠️  CRITICAL: Password appears in response!")
        else:
            print("✓  Password not disclosed in response")


class TestRateLimitingEffectiveness:
    """Test rate limiting implementation"""
    
    def test_rate_limit_bypass_attempts(self):
        """
        Attempt to bypass rate limiting using various techniques
        
        Tests: Rate limiting robustness
        """
        user = {
            "email": "ratelimit@example.com",
            "password": "SecurePass123!",
            "full_name": "Rate Limit Test"
        }
        client.post("/api/auth/register", json=user)
        
        print(f"\n[RATE LIMIT BYPASS TEST]")
        
        # Technique 1: Rapid sequential requests
        print("\nTechnique 1: Rapid sequential requests")
        blocked_count = 0
        for i in range(20):
            response = client.post("/api/auth/login", json={
                "email": user["email"],
                "password": "wrongpassword"
            })
            if response.status_code == 429:
                blocked_count += 1
        
        print(f"Blocked: {blocked_count}/20")
        if blocked_count == 0:
            print("⚠️  No rate limiting detected")
        else:
            print(f"✓  Rate limiting active")
        
        # Technique 2: Requests with different User-Agent headers
        print("\nTechnique 2: Different User-Agent headers")
        bypassed = False
        for i in range(10):
            response = client.post(
                "/api/auth/login",
                json={"email": user["email"], "password": "wrongpassword"},
                headers={"User-Agent": f"Browser{i}"}
            )
            if response.status_code == 200:
                bypassed = True
                break
        
        if bypassed:
            print("⚠️  Rate limit bypassed with different User-Agent")
        else:
            print("✓  User-Agent bypass prevented")


# Vulnerability Summary Report
def generate_vulnerability_report():
    """Generate a summary report of found vulnerabilities"""
    print("\n" + "="*70)
    print("SECURITY PENETRATION TEST SUMMARY")
    print("="*70)
    print("\nRun the test suite to generate a detailed vulnerability report:")
    print("  pytest test_security_penetration.py -v --tb=short")
    print("\nCritical vulnerabilities to address:")
    print("  1. VULN-HIGH-001: No Rate Limiting")
    print("  2. VULN-HIGH-002: No JWT Token Blacklist")
    print("  3. VULN-CRIT-001: No HTTPS Enforcement")
    print("\nRefer to SECURITY_VULNERABILITIES.md for detailed remediation steps.")
    print("="*70 + "\n")


if __name__ == "__main__":
    generate_vulnerability_report()
    pytest.main([__file__, "-v", "--tb=short"])
