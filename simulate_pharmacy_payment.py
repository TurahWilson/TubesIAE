
import requests
import json

PRESC_ID = 1
URL = f"http://localhost:8000/api/prescriptions/{PRESC_ID}"

def complete_payment():
    payload = {
        "status": "processed"
    }
    
    # We use PUT to update. 
    # Note: schema.PrescriptionUpdate allows partial updates because fields are Optional.
    # However, since we are sending JSON, we need to ensure the service handles partial fields correctly 
    # (which we verified in code: if update_data.status: ...)
    
    try:
        response = requests.put(URL, json=payload)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Update Success!")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Update Failed: {response.text}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    complete_payment()
