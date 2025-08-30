#!/usr/bin/env python3
"""
Test the Indian Banking Fraud Detection System
"""

import requests
import json

API_BASE = "http://localhost:8001"

def test_api_health():
    """Test if the API is running"""
    try:
        response = requests.get(f"{API_BASE}/")
        print("🏥 Health Check:")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_single_prediction():
    """Test single transaction prediction with Indian banking features"""
    print("\n🔍 Testing Single Transaction Prediction:")
    
    # Test cases with Indian banking scenarios
    test_cases = [
        {
            "name": "Normal UPI Payment",
            "data": {
                "Amount": 1500,
                "Payment_Method": "UPI",
                "Merchant_Category": "Food",
                "Location": "Mumbai",
                "Time": "2024-01-15T14:30:00"
            }
        },
        {
            "name": "High Amount RTGS",
            "data": {
                "Amount": 950000,
                "Payment_Method": "RTGS",
                "Merchant_Category": "Others",
                "Location": "Delhi",
                "Time": "2024-01-15T02:30:00"  # Night transaction
            }
        },
        {
            "name": "International Card Payment",
            "data": {
                "Amount": 75000,
                "Payment_Method": "Card",
                "Merchant_Category": "Entertainment",
                "Location": "Bangalore"
            }
        },
        {
            "name": "Small NEFT Payment",
            "data": {
                "Amount": 250,
                "Payment_Method": "NEFT",
                "Merchant_Category": "Utilities",
                "Location": "Chennai"
            }
        }
    ]
    
    for test_case in test_cases:
        try:
            response = requests.post(f"{API_BASE}/predict", json=test_case["data"])
            if response.status_code == 200:
                result = response.json()
                fraud_status = "🚨 FRAUD" if result["is_fraud"] else "✅ LEGITIMATE"
                probability = result["probability"] * 100
                
                print(f"\n📝 {test_case['name']}:")
                print(f"   Amount: ₹{test_case['data']['Amount']:,}")
                print(f"   Method: {test_case['data']['Payment_Method']}")
                print(f"   Category: {test_case['data']['Merchant_Category']}")
                print(f"   Location: {test_case['data']['Location']}")
                print(f"   Result: {fraud_status}")
                print(f"   Probability: {probability:.2f}%")
                
                if "details" in result:
                    print(f"   Model: {result['details'].get('model', 'Unknown')}")
                
            else:
                print(f"❌ {test_case['name']} failed: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"❌ {test_case['name']} error: {e}")

def test_batch_prediction():
    """Test batch prediction by creating a sample CSV"""
    print("\n📁 Testing Batch Prediction:")
    
    # Create a sample CSV file
    import pandas as pd
    
    sample_data = [
        {"Amount": 1500, "Payment_Method": "UPI", "Merchant_Category": "Food", "Location": "Mumbai"},
        {"Amount": 85000, "Payment_Method": "NEFT", "Merchant_Category": "Others", "Location": "Delhi"},
        {"Amount": 250000, "Payment_Method": "Card", "Merchant_Category": "Entertainment", "Location": "Goa"},
        {"Amount": 750, "Payment_Method": "IMPS", "Merchant_Category": "Transport", "Location": "Pune"},
        {"Amount": 125000, "Payment_Method": "RTGS", "Merchant_Category": "Healthcare", "Location": "Chennai"}
    ]
    
    df = pd.DataFrame(sample_data)
    csv_file = "test_transactions.csv"
    df.to_csv(csv_file, index=False)
    
    try:
        with open(csv_file, 'rb') as f:
            files = {'file': (csv_file, f, 'text/csv')}
            response = requests.post(f"{API_BASE}/upload", files=files)
            
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Batch prediction successful!")
            print(f"   Total transactions: {result['summary']['total']}")
            print(f"   Fraudulent: {result['summary']['fraudulent']}")
            print(f"   Legitimate: {result['summary']['legit']}")
            
            # Show first few results
            print("\n📊 Sample Results:")
            for i, res in enumerate(result['results'][:3]):
                fraud_status = "🚨 FRAUD" if res["is_fraud"] else "✅ LEGIT"
                probability = res["probability"] * 100
                print(f"   Transaction {res['transaction_id']}: {fraud_status} ({probability:.1f}%)")
        else:
            print(f"❌ Batch prediction failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Batch prediction error: {e}")
    
    # Clean up
    import os
    if os.path.exists(csv_file):
        os.remove(csv_file)

def main():
    """Run all tests"""
    print("🇮🇳 Indian Banking Fraud Detection System Test")
    print("=" * 50)
    
    # Test API health
    if not test_api_health():
        print("❌ API is not running. Please start the backend server first.")
        return
    
    # Test single predictions
    test_single_prediction()
    
    # Test batch predictions
    test_batch_prediction()
    
    print("\n" + "=" * 50)
    print("🎉 Testing completed!")
    print("\n💡 Tips:")
    print("   • Open http://localhost:3000 to access the web interface")
    print("   • Try different payment methods: UPI, NEFT, RTGS, IMPS, Card")
    print("   • Higher amounts and night transactions increase fraud probability")
    print("   • Card and Net Banking are considered higher risk payment methods")

if __name__ == "__main__":
    main()
