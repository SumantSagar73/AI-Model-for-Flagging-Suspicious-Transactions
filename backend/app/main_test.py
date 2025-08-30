# Quick test script for FastAPI endpoints
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_predict():
    data = {"amount": 100, "time": 12345}
    response = client.post("/predict", json=data)
    print("/predict response:", response.json())

def test_upload():
    import io
    import pandas as pd
    df = pd.DataFrame({"amount": [100, 200], "time": [12345, 23456]})
    csv_bytes = io.StringIO()
    df.to_csv(csv_bytes, index=False)
    csv_bytes.seek(0)
    files = {"file": ("test.csv", csv_bytes.getvalue())}
    response = client.post("/upload", files=files)
    print("/upload response:", response.json())

if __name__ == "__main__":
    test_predict()
    test_upload()
