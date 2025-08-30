"""
Create realistic synthetic banking transaction data
This simulates real-world banking patterns and fraud indicators
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_realistic_transactions(n_samples=50000):
    np.random.seed(42)
    
    print("Creating realistic banking transaction dataset...")
    
    # Time patterns (business hours, weekends, holidays)
    start_date = datetime(2024, 1, 1)
    dates = []
    amounts = []
    merchants = []
    locations = []
    fraud_labels = []
    
    # Merchant categories
    merchant_types = [
        'Grocery Store', 'Gas Station', 'Restaurant', 'Online Retailer', 
        'ATM Withdrawal', 'Department Store', 'Pharmacy', 'Coffee Shop',
        'Hotel', 'Airlines', 'Utility Payment', 'Insurance', 'Bank Transfer'
    ]
    
    # Location patterns
    home_locations = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
    foreign_locations = ['London', 'Tokyo', 'Paris', 'Dubai', 'Sydney']
    
    features = {}
    for i in range(1, 29):
        features[f'V{i}'] = []
    
    for i in range(n_samples):
        # Time patterns
        days_offset = int(np.random.randint(0, 365))
        hour = int(np.random.choice(range(24), p=create_hour_probability()))
        transaction_time = start_date + timedelta(days=days_offset, hours=hour)
        
        # Determine if fraud (5% base rate, higher at night/weekends)
        fraud_probability = 0.02  # Base 2%
        if hour < 6 or hour > 22:  # Night transactions more risky
            fraud_probability *= 3
        if transaction_time.weekday() >= 5:  # Weekend slightly more risky
            fraud_probability *= 1.5
            
        is_fraud = np.random.random() < fraud_probability
        
        # Amount patterns
        if is_fraud:
            # Fraudulent transactions: often very small (testing) or very large
            if np.random.random() < 0.3:
                amount = np.random.uniform(1, 10)  # Small test amounts
            else:
                amount = np.random.exponential(500) + 100  # Large amounts
        else:
            # Normal transactions follow different patterns by merchant
            merchant = np.random.choice(merchant_types)
            if merchant == 'Grocery Store':
                amount = np.random.gamma(2, 30)  # $60 average
            elif merchant == 'Gas Station':
                amount = np.random.gamma(3, 15)  # $45 average
            elif merchant == 'Restaurant':
                amount = np.random.gamma(2, 20)  # $40 average
            elif merchant == 'ATM Withdrawal':
                amount = np.random.choice([20, 40, 60, 80, 100, 200])
            else:
                amount = np.random.exponential(50) + 5
        
        # Location patterns
        if is_fraud and np.random.random() < 0.4:
            location = np.random.choice(foreign_locations)  # Fraud often from unusual locations
        else:
            location = np.random.choice(home_locations)
        
        # Feature engineering (V1-V28) - these represent anonymized transaction features
        for j in range(1, 29):
            if is_fraud:
                # Fraudulent transactions have different statistical patterns
                if j <= 10:
                    features[f'V{j}'].append(np.random.normal(0.5, 1.5))  # Shifted mean
                else:
                    features[f'V{j}'].append(np.random.normal(-0.3, 1.2))
            else:
                # Normal transactions
                features[f'V{j}'].append(np.random.normal(0, 1))
        
        dates.append(transaction_time)
        amounts.append(min(amount, 25000))  # Cap at $25K
        merchants.append(merchant)
        locations.append(location)
        fraud_labels.append(1 if is_fraud else 0)
    
    # Create DataFrame
    df = pd.DataFrame(features)
    df['Time'] = [(d - start_date).total_seconds() for d in dates]
    df['Amount'] = amounts
    df['Merchant_Type'] = merchants
    df['Location'] = locations
    df['Class'] = fraud_labels
    
    # Add derived features that banks actually use
    df['Hour'] = [d.hour for d in dates]
    df['Day_of_Week'] = [d.weekday() for d in dates]
    df['Is_Weekend'] = df['Day_of_Week'] >= 5
    df['Is_Night'] = (df['Hour'] < 6) | (df['Hour'] > 22)
    
    return df

def create_hour_probability():
    # More transactions during business hours
    probs = np.ones(24) * 0.02  # Base probability
    probs[6:22] = 0.06  # Business hours
    probs[12:14] = 0.08  # Lunch peak
    probs[17:19] = 0.08  # Evening peak
    return probs / probs.sum()

if __name__ == "__main__":
    # Create realistic dataset
    df = create_realistic_transactions(50000)
    
    # Save dataset
    df.to_csv('realistic_transactions.csv', index=False)
    
    print(f"Created realistic dataset with {len(df)} transactions")
    print(f"Fraud rate: {df['Class'].mean():.3%}")
    print(f"Average transaction amount: ${df['Amount'].mean():.2f}")
    print(f"Fraud cases: {df['Class'].sum()}")
    print("\nMerchant distribution:")
    print(df['Merchant_Type'].value_counts())
    print("\nSample data:")
    print(df.head())
