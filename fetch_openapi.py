import requests
import json

url = "https://92a0e4ea-c2f1-4418-a38c-8a295310ccae-00-2gpabn86re6nk.riker.replit.dev/openapi.json"

try:
    print(f"Fetching {url}")
    response = requests.get(url)
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
        with open("external_openapi.json", "w") as f:
            f.write(json.dumps(response.json(), indent=2))
    else:
        print(f"Failed: {response.status_code}")
except Exception as e:
    print(f"Error: {e}")
