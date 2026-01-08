import requests
import json

url = "https://92a0e4ea-c2f1-4418-a38c-8a295310ccae-00-2gpabn86re6nk.riker.replit.dev/graphql"
query = """
{
  __schema {
    queryType {
      fields {
        name
        args {
          name
        }
      }
    }
  }
}
"""

try:
    print(f"Introspecting {url} with GET")
    response = requests.get(url, params={"query": query})
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(response.text)
except Exception as e:
    print(f"Error: {e}")
