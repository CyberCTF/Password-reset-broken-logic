import requests
import sys

def test_application():
    base_url = "http://localhost:3206"
    
    print("🧪 Testing TechCorp Inventory Application...")
    print("=" * 50)
    
    # Test 1: Page d'accueil (redirection vers login)
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Homepage (/) - Status: {response.status_code}")
        if response.status_code != 200:
            print(f"❌ Expected 200, got {response.status_code}")
    except Exception as e:
        print(f"❌ Homepage (/) - Error: {e}")
    
    # Test 2: Page de login
    try:
        response = requests.get(f"{base_url}/login")
        print(f"✅ Login page (/login) - Status: {response.status_code}")
        # Vérifier que la page ne contient plus la liste des utilisateurs
        if "System Users" in response.text:
            print("❌ User list still present in login page!")
        else:
            print("✅ User list successfully removed from login page")
    except Exception as e:
        print(f"❌ Login page (/login) - Error: {e}")
    
    # Test 3: Page d'inscription (nouvelle)
    try:
        response = requests.get(f"{base_url}/register")
        print(f"✅ Register page (/register) - Status: {response.status_code}")
        # Vérifier que c'est bien le formulaire simplifié
        if "first_name" in response.text or "email" in response.text:
            print("❌ Old registration form still present!")
        else:
            print("✅ Simplified registration form working")
    except Exception as e:
        print(f"❌ Register page (/register) - Error: {e}")
    
    # Test 4: Page forgot password
    try:
        response = requests.get(f"{base_url}/forgot-password")
        print(f"✅ Forgot password (/forgot-password) - Status: {response.status_code}")
        # Vérifier que le champ current_password est présent
        if "current_password" in response.text:
            print("✅ Current password field added successfully")
        else:
            print("❌ Current password field missing!")
    except Exception as e:
        print(f"❌ Forgot password (/forgot-password) - Error: {e}")
    
    # Test 5: Thème dark mode
    try:
        response = requests.get(f"{base_url}/login")
        if "#000000" in response.text or "background: #000000" in response.text:
            print("✅ Full dark mode theme applied")
        else:
            print("⚠️  Dark mode theme may not be fully applied")
    except Exception as e:
        print(f"❌ Theme test - Error: {e}")
    
    print("=" * 50)
    print("🏁 Tests completed!")

if __name__ == "__main__":
    test_application()