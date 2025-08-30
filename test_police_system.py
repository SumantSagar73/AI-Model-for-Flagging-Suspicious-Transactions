#!/usr/bin/env python3
"""
Test the Police Financial Crime Investigation System
"""

import requests
import json

API_BASE = "http://localhost:8001"

def test_api_health():
    """Test if the police API is running"""
    try:
        response = requests.get(f"{API_BASE}/")
        print("🚔 Police System Health Check:")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Department: {result.get('department', 'Unknown')}")
        print(f"Unit: {result.get('jurisdiction', 'Unknown')}")
        print(f"System: {result.get('message', 'Unknown')}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Police system health check failed: {e}")
        return False

def test_police_investigation():
    """Test single case investigation with police scenarios"""
    print("\n🕵️ Testing Police Case Investigation:")
    
    # Test cases with police investigation scenarios
    test_cases = [
        {
            "name": "Complaint Case - Small UPI Transfer",
            "data": {
                "Amount": 2500,
                "Payment_Method": "UPI",
                "Merchant_Category": "Food",
                "Location": "Mumbai",
                "Time": "2024-01-15T14:30:00"
            }
        },
        {
            "name": "FIR Case - High Value RTGS at Night",
            "data": {
                "Amount": 875000,
                "Payment_Method": "RTGS",
                "Merchant_Category": "Others",
                "Location": "Delhi",
                "Time": "2024-01-15T02:30:00"  # Night transaction
            }
        },
        {
            "name": "Bank Report - Suspicious Card Payment",
            "data": {
                "Amount": 125000,
                "Payment_Method": "Card",
                "Merchant_Category": "Entertainment",
                "Location": "Goa"
            }
        },
        {
            "name": "Routine Check - NEFT Payment",
            "data": {
                "Amount": 15000,
                "Payment_Method": "NEFT",
                "Merchant_Category": "Healthcare",
                "Location": "Chennai"
            }
        },
        {
            "name": "Cybercrime Case - Large Online Transfer",
            "data": {
                "Amount": 450000,
                "Payment_Method": "Net Banking",
                "Merchant_Category": "Others",
                "Location": "Bangalore",
                "Time": "2024-01-15T23:45:00"
            }
        }
    ]
    
    high_priority_cases = 0
    medium_priority_cases = 0
    low_priority_cases = 0
    
    for test_case in test_cases:
        try:
            response = requests.post(f"{API_BASE}/predict", json=test_case["data"])
            if response.status_code == 200:
                result = response.json()
                fraud_status = "🚨 INVESTIGATE" if result["is_fraud"] else "✅ ROUTINE"
                probability = result["probability"] * 100
                priority = result["details"].get("investigation_priority", "UNKNOWN")
                recommendation = result["details"].get("recommendation", "No recommendation")
                
                print(f"\n📝 {test_case['name']}:")
                print(f"   Amount: ₹{test_case['data']['Amount']:,}")
                print(f"   Method: {test_case['data']['Payment_Method']}")
                print(f"   Category: {test_case['data']['Merchant_Category']}")
                print(f"   Location: {test_case['data']['Location']}")
                print(f"   Assessment: {fraud_status}")
                print(f"   Risk Score: {probability:.2f}%")
                print(f"   Priority: {priority}")
                print(f"   Action: {recommendation}")
                
                # Count priorities
                if priority == "HIGH":
                    high_priority_cases += 1
                elif priority == "MEDIUM":
                    medium_priority_cases += 1
                elif priority == "LOW":
                    low_priority_cases += 1
                
            else:
                print(f"❌ {test_case['name']} failed: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"❌ {test_case['name']} error: {e}")
    
    # Summary for police
    print(f"\n📊 INVESTIGATION SUMMARY:")
    print(f"   🔴 HIGH Priority Cases: {high_priority_cases}")
    print(f"   🟡 MEDIUM Priority Cases: {medium_priority_cases}")
    print(f"   🟢 LOW Priority Cases: {low_priority_cases}")
    print(f"   📁 Total Cases Analyzed: {len(test_cases)}")

def test_bulk_case_analysis():
    """Test bulk case analysis for police department"""
    print("\n📁 Testing Bulk Case Analysis:")
    
    # Create a sample CSV file with police case data
    import pandas as pd
    
    case_data = [
        {"Amount": 3500, "Payment_Method": "UPI", "Merchant_Category": "Food", "Location": "Mumbai"},
        {"Amount": 150000, "Payment_Method": "NEFT", "Merchant_Category": "Others", "Location": "Delhi"},
        {"Amount": 750000, "Payment_Method": "Card", "Merchant_Category": "Entertainment", "Location": "Goa"},
        {"Amount": 25000, "Payment_Method": "IMPS", "Merchant_Category": "Transport", "Location": "Pune"},
        {"Amount": 890000, "Payment_Method": "RTGS", "Merchant_Category": "Others", "Location": "Chennai"},
        {"Amount": 8000, "Payment_Method": "UPI", "Merchant_Category": "Healthcare", "Location": "Kolkata"},
        {"Amount": 320000, "Payment_Method": "Net Banking", "Merchant_Category": "Others", "Location": "Hyderabad"},
        {"Amount": 1200, "Payment_Method": "UPI", "Merchant_Category": "Retail", "Location": "Jaipur"}
    ]
    
    df = pd.DataFrame(case_data)
    csv_file = "police_case_batch.csv"
    df.to_csv(csv_file, index=False)
    
    try:
        with open(csv_file, 'rb') as f:
            files = {'file': (csv_file, f, 'text/csv')}
            response = requests.post(f"{API_BASE}/upload", files=files)
            
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Bulk case analysis successful!")
            print(f"   Total cases processed: {result['summary']['total']}")
            print(f"   High-risk cases: {result['summary']['fraudulent']}")
            print(f"   Routine cases: {result['summary']['legit']}")
            print(f"   Investigation rate: {(result['summary']['fraudulent']/result['summary']['total']*100):.1f}%")
            
            # Show priority breakdown
            print("\n📊 Case Priority Analysis:")
            high_priority = sum(1 for res in result['results'] if res['probability'] > 0.7)
            medium_priority = sum(1 for res in result['results'] if 0.3 < res['probability'] <= 0.7)
            low_priority = sum(1 for res in result['results'] if res['probability'] <= 0.3)
            
            print(f"   🔴 HIGH Priority: {high_priority} cases")
            print(f"   🟡 MEDIUM Priority: {medium_priority} cases")
            print(f"   🟢 LOW Priority: {low_priority} cases")
            
            # Show first few high-priority cases
            high_risk_cases = [res for res in result['results'] if res['probability'] > 0.5]
            if high_risk_cases:
                print(f"\n🚨 HIGH-RISK CASES REQUIRING IMMEDIATE ATTENTION:")
                for i, case in enumerate(high_risk_cases[:3], 1):
                    print(f"   Case {case['transaction_id']:03d}: {case['probability']*100:.1f}% fraud risk")
        else:
            print(f"❌ Bulk case analysis failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Bulk case analysis error: {e}")
    
    # Clean up
    import os
    if os.path.exists(csv_file):
        os.remove(csv_file)

def main():
    """Run all police system tests"""
    print("🚔 POLICE FINANCIAL CRIME INVESTIGATION SYSTEM TEST")
    print("=" * 60)
    
    # Test API health
    if not test_api_health():
        print("❌ Police system is not running. Please start the backend server first.")
        return
    
    # Test individual case investigations
    test_police_investigation()
    
    # Test bulk case analysis
    test_bulk_case_analysis()
    
    print("\n" + "=" * 60)
    print("🎉 Police System Testing Completed!")
    print("\n💼 POLICE USAGE INSTRUCTIONS:")
    print("   • Web Dashboard: http://localhost:3000")
    print("   • Use 'Case Upload' tab for bulk case analysis from bank reports")
    print("   • Use 'Transaction Check' tab for individual complaint investigation")
    print("   • High-risk cases require immediate investigation")
    print("   • Medium-risk cases need further verification")
    print("   • Low-risk cases can be processed routinely")
    print("\n🔧 INTEGRATION OPTIONS:")
    print("   • API can be integrated with police case management systems")
    print("   • Export results to Excel for case documentation")
    print("   • Set up automated alerts for high-risk transactions")

if __name__ == "__main__":
    main()
