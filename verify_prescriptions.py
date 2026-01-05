import requests
import json
import sys

BASE_URL = "http://localhost:8000/api/prescriptions"

def test_crud():
    print("Testing Prescription CRUD...")

    # 1. CREATE
    print("\n[1] Creating new prescription...")
    payload = {
        "patientName": "Budi Santoso",
        "doctorName": "dr. Strange",
        "status": "pending",
        "items": [
            { "medicineId": 101, "medicineName": "Paracetamol", "quantity": 10, "instructions": "3x1 sesudah makan" },
            { "medicineId": 102, "medicineName": "Amoxicillin", "quantity": 5, "instructions": "Habiskan" }
        ]
    }
    try:
        response = requests.post(BASE_URL, json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        if response.status_code != 200:
            print("FAILED to create")
            return
        data = response.json()
        prescription_id = data["id"]
        print(f"Created ID: {prescription_id}")
    except Exception as e:
        print(f"Error: {e}")
        return

    # 2. GET ALL
    print("\n[2] Getting all prescriptions...")
    try:
        response = requests.get(BASE_URL)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Count: {len(response.json())}")
            print(f"Data: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

    # 3. GET ONE
    print(f"\n[3] Getting prescription {prescription_id}...")
    try:
        response = requests.get(f"{BASE_URL}/{prescription_id}")
        print(f"Status: {response.status_code}")
        print(f"Data: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

    # 4. UPDATE
    print(f"\n[4] Updating prescription {prescription_id}...")
    update_payload = {
        "status": "processed",
        "items": [
            { "medicineId": 101, "medicineName": "Paracetamol", "quantity": 15, "instructions": "3x1 sesudah makan (Ditambah)" }
        ]
    }
    try:
        response = requests.put(f"{BASE_URL}/{prescription_id}", json=update_payload)
        print(f"Status: {response.status_code}")
        print(f"Data: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

    # 5. DELETE
    # print(f"\n[5] Deleting prescription {prescription_id}...")
    # try:
    #     response = requests.delete(f"{BASE_URL}/{prescription_id}")
    #     print(f"Status: {response.status_code}")
    #     print(f"Response: {response.text}")
    # except Exception as e:
    #     print(f"Error: {e}")

if __name__ == "__main__":
    test_crud()
