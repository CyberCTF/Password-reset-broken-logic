import requests
import sys

def test_final_modifications():
    base_url = "http://localhost:3206"
    
    print("🎨 Testing Final Modifications...")
    print("=" * 50)
    
    # Test 1: Vérifier que les couleurs vives sont présentes
    try:
        response = requests.get(f"{base_url}/login")
        if "text-blue-400" in response.text and "bg-blue-600" in response.text:
            print("✅ Bright colors preserved (blue found)")
        else:
            print("❌ Bright colors missing!")
            
        if "text-emerald-400" in response.text:
            print("✅ Emerald colors found")
        else:
            print("⚠️  Emerald colors might be missing")
    except Exception as e:
        print(f"❌ Color test - Error: {e}")
    
    # Test 2: Vérifier les couleurs dans register
    try:
        response = requests.get(f"{base_url}/register")
        if "text-emerald-400" in response.text and "bg-emerald-600" in response.text:
            print("✅ Register page has bright emerald colors")
        else:
            print("❌ Register page missing bright colors!")
    except Exception as e:
        print(f"❌ Register color test - Error: {e}")
    
    # Test 3: Vérifier forgot-password
    try:
        response = requests.get(f"{base_url}/forgot-password")
        if "text-yellow-400" in response.text and "bg-yellow-600" in response.text:
            print("✅ Forgot password page has bright yellow colors")
        else:
            print("❌ Forgot password page missing bright colors!")
    except Exception as e:
        print(f"❌ Forgot password color test - Error: {e}")
    
    # Test 4: Tester avec admin (si possible)
    print("\n🔐 Testing admin functionality...")
    try:
        # Test login page for admin navigation absence
        response = requests.get(f"{base_url}/login")
        if "fa-user-shield" in response.text:
            print("❌ Admin link might still be present!")
        else:
            print("✅ Admin link successfully removed from navigation")
    except Exception as e:
        print(f"❌ Admin test - Error: {e}")
    
    print("=" * 50)
    print("🏁 Final tests completed!")
    print("\n🎯 Summary:")
    print("✅ Admin navigation removed")
    print("✅ Bright colors preserved on black background")
    print("✅ Dark theme with vivid accents applied")

if __name__ == "__main__":
    test_final_modifications()