#!/usr/bin/env python3

import requests
import json

def test_registration():
    """Test the registration functionality"""
    
    base_url = "http://localhost:3206"
    
    print("=== Test d'inscription ===")
    
    # Test 1: Inscription normale
    print("\n1. Test d'inscription normale:")
    registration_data = {
        'username': 'testuser123',
        'password': 'password123',
        'confirm_password': 'password123'
    }
    
    response = requests.post(f"{base_url}/register", data=registration_data, allow_redirects=False)
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 302:
        print("   ✅ Redirection détectée (probablement vers login) - Inscription réussie")
        location = response.headers.get('Location', '')
        print(f"   Redirection vers: {location}")
    elif response.status_code == 200:
        if "Account created successfully" in response.text:
            print("   ✅ Message de succès trouvé")
        elif "error" in response.text.lower():
            print("   ❌ Erreur détectée dans la réponse")
            # Extraire le message d'erreur si possible
            if "An error occurred while creating your account" in response.text:
                print("   Erreur: Problème lors de la création du compte")
        else:
            print("   ⚠️  Statut 200 mais contenu ambigu")
    else:
        print(f"   ❌ Statut inattendu: {response.status_code}")
    
    # Test 2: Vérifier qu'on peut se connecter avec le nouveau compte
    print("\n2. Test de connexion avec le nouveau compte:")
    login_data = {
        'username': 'testuser123',
        'password': 'password123'
    }
    
    response = requests.post(f"{base_url}/login", data=login_data, allow_redirects=False)
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 302:
        print("   ✅ Connexion réussie (redirection vers dashboard)")
    else:
        print("   ❌ Échec de la connexion")
    
    # Test 3: Tentative d'inscription avec username existant
    print("\n3. Test d'inscription avec username existant:")
    response = requests.post(f"{base_url}/register", data=registration_data, allow_redirects=False)
    print(f"   Status Code: {response.status_code}")
    
    if "Username already exists" in response.text:
        print("   ✅ Message d'erreur approprié pour username existant")
    else:
        print("   ⚠️  Pas de message d'erreur pour username existant")

if __name__ == "__main__":
    test_registration()