import requests

base_url = "https://92a0e4ea-c2f1-4418-a38c-8a295310ccae-00-2gpabn86re6nk.riker.replit.dev"
paths = [
    "/graphql",
    "/api/graphql",
    "/v1/graphql",
    "/graph",
    "/api/graph",
    "/graphql/" # Trailing slash
]

for path in paths:
    url = base_url + path
    print(f"Checking {url}")
    try:
        # Try GET (often returns Playground HTML)
        resp = requests.get(url, timeout=3)
        print(f"GET {path}: {resp.status_code}")
        
        # Try POST (introspection)
        resp = requests.post(url, json={"query": "{__typename}"}, timeout=3)
        print(f"POST {path}: {resp.status_code}")
    except Exception as e:
        print(f"Error {path}: {e}")
