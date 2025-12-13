import requests
import json

def check_patent_api():
    molecule = "Metformin" # Test case
    print(f"Testing Patent API for {molecule}...")
    
    # 1. Granted
    url_granted = "https://api.patentsview.org/patents/query"
    query_granted = {"_text_any": {"patent_title": [molecule]}}
    params_granted = {
        "q": json.dumps(query_granted),
        "f": '["patent_number", "patent_date", "patent_title"]'
    }
    try:
        resp = requests.get(url_granted, params=params_granted, timeout=10)
        print(f"Granted API: {resp.status_code}")
        if resp.status_code == 200:
            print(f"Granted Data Sample: {str(resp.json())[:100]}...")
        else:
            print(f"Granted API Error: {resp.text}")
    except Exception as e:
        print(f"Granted API Exception: {e}")

    # 2. Applications
    url_apps = "https://api.patentsview.org/pregrant_publications/query"
    query_apps = {"_text_any": {"pgpub_title": [molecule]}}
    params_apps = {
        "q": json.dumps(query_apps),
        "f": '["pgpub_id", "pgpub_publish_date", "pgpub_title"]'
    }
    try:
        resp_apps = requests.get(url_apps, params=params_apps, timeout=10)
        print(f"Apps API: {resp_apps.status_code}")
        if resp_apps.status_code == 200:
            print(f"Apps Data Sample: {str(resp_apps.json())[:100]}...")
        else:
            print(f"Apps API Error: {resp_apps.text}")
    except Exception as e:
        print(f"Apps API Exception: {e}")

if __name__ == "__main__":
    check_patent_api()
