import requests
import json
import time

def test_api():
    url = "http://127.0.0.1:8001/predict"
    data = {"V1": 1.0, "V2": -1.0, "V3": 0.5, "V4": 0.2, "V5": -0.8, "V6": 1.2, "V7": 0.3, "V8": -0.7, "V9": 0.9, "V10": -0.4, "V11": 0.6, "V12": -0.3, "V13": 0.8, "V14": -0.6, "V15": 0.4, "V16": -0.9, "V17": 0.7, "V18": -0.2, "V19": 0.1, "V20": -0.5, "V21": 0.3, "V22": -0.8, "V23": 0.6, "V24": -0.1, "V25": 0.9, "V26": -0.7, "V27": 0.2, "V28": -0.4, "Time": 12345, "Amount": 100.50}
    
    try:
        print("Testing API...")
        response = requests.post(url, json=data, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Backend not running or connection failed")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_api()
