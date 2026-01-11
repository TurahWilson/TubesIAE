"""
Test script untuk verify endpoint /verify-token
"""
import requests

# Test 1: Call verify-token WITHOUT authorization header
print("Test 1: No Authorization Header")
try:
    response = requests.post("http://localhost:8001/verify-token")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*50 + "\n")

# Test 2: Call verify-token WITH authorization header (fake token)
print("Test 2: With Fake Token")
try:
    response = requests.post(
        "http://localhost:8001/verify-token",
        headers={"Authorization": "Bearer fake_token_123"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*50 + "\n")

# Test 3: First login to get real token, then verify
print("Test 3: Login and Verify Real Token")
try:
    # Login
    login_data = {
        "username": "admin@hospital.com",  # Change this to your actual admin email
        "password": "admin123"  # Change this to your actual password
    }
    login_response = requests.post(
        "http://localhost:8001/token",
        data=login_data
    )
    
    if login_response.status_code == 200:
        token_data = login_response.json()
        access_token = token_data.get("access_token")
        print(f"Login successful! Token: {access_token[:20]}...")
        
        # Now verify the token
        verify_response = requests.post(
            "http://localhost:8001/verify-token",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        print(f"Verify Status: {verify_response.status_code}")
        print(f"Verify Response: {verify_response.json()}")
    else:
        print(f"Login failed: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        
except Exception as e:
    print(f"Error: {e}")
