# test_connection.py
import requests
from network_config import COUNCIL_MEMBERS, CHAIRMAN

def test_endpoint(entity):
    try:
        # Test basic connectivity
        tags_response = requests.get(f"{entity['ip']}/api/tags")
        if tags_response.status_code != 200:
            print(f"❌ Failed basic connection to {entity['name']}: HTTP {tags_response.status_code}")
            return

        # Check if model is available
        models = [m['name'] for m in tags_response.json().get('models', [])]
        if not any(entity['model'] in m for m in models):
            print(f"⚠️ Model '{entity['model']}' not found on {entity['name']}. Pull it with 'ollama pull {entity['model']}'.")
        else:
            print(f"✅ Model '{entity['model']}' available on {entity['name']}.")

        # Test /api/generate with dummy payload
        payload = {"model": entity['model'], "prompt": "Test connection", "stream": False}
        gen_response = requests.post(f"{entity['ip']}/api/generate", json=payload)
        if gen_response.status_code == 200:
            print(f"✅ Success! /api/generate works for {entity['name']}.")
        else:
            print(f"❌ /api/generate failed for {entity['name']}: HTTP {gen_response.status_code}")
    except Exception as e:
        print(f"⚠️ Error reaching {entity['name']}: {e}")

# Test members
for member in COUNCIL_MEMBERS:
    test_endpoint(member)

# Test chairman
test_endpoint(CHAIRMAN)