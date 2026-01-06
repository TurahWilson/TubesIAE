
import requests
import json

BASE_URL = "http://localhost:8000/api/prescriptions"

def list_prescriptions():
    try:
        response = requests.get(BASE_URL)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Prescriptions:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    list_prescriptions()
