"""
Indian Banking Fraud Detection Dataset Generator
Creates realistic Indian banking transaction patterns with:
- UPI, RTGS, NEFT, IMPS payment methods
- Indian merchant categories
- Regional patterns across Indian states
- Festival and seasonal spending patterns
- RBI compliance indicators
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def create_indian_banking_dataset(n_samples=100000):
    np.random.seed(42)
    random.seed(42)
    
    print("Creating Indian Banking Transaction Dataset...")
    
    # Indian Payment Methods
    payment_methods = [
        'UPI', 'RTGS', 'NEFT', 'IMPS', 'Debit_Card', 'Credit_Card', 
        'Net_Banking', 'Mobile_Banking', 'ATM_Withdrawal', 'Cash_Deposit'
    ]
    
    # Indian Merchant Categories
    indian_merchants = [
        'Grocery_Kirana', 'Petrol_Pump', 'Restaurant_Dhaba', 'E_Commerce', 
        'Mobile_Recharge', 'Electricity_Bill', 'Gas_Cylinder', 'Medical_Pharmacy',
        'Gold_Jewellery', 'Clothing_Textile', 'Auto_Rickshaw', 'Train_Booking',
        'Bus_Booking', 'Movie_Ticket', 'DTH_Recharge', 'Insurance_Premium',
        'Mutual_Fund', 'Fixed_Deposit', 'Education_Fee', 'Temple_Donation'
    ]
    
    # Indian States and Cities
    indian_locations = [
        'Mumbai_Maharashtra', 'Delhi_NCR', 'Bangalore_Karnataka', 'Chennai_Tamil_Nadu',
        'Kolkata_West_Bengal', 'Hyderabad_Telangana', 'Pune_Maharashtra', 'Ahmedabad_Gujarat',
        'Jaipur_Rajasthan', 'Lucknow_Uttar_Pradesh', 'Kochi_Kerala', 'Indore_Madhya_Pradesh',
        'Bhubaneswar_Odisha', 'Guwahati_Assam', 'Chandigarh_Punjab', 'Coimbatore_Tamil_Nadu'
    ]
    
    # Suspicious locations (for fraud simulation)
    suspicious_locations = [
        'International_Dubai', 'International_Singapore', 'International_USA',
        'Border_Nepal', 'Border_Bangladesh', 'Unknown_Location'
    ]
    
    # Indian Banking Hours (10 AM to 4 PM for traditional banking)
    banking_hours = list(range(10, 16))
    
    # Festival dates (higher transaction volumes)
    festivals = [
        datetime(2024, 3, 8),   # Holi
        datetime(2024, 4, 17),  # Ram Navami
        datetime(2024, 8, 19),  # Raksha Bandhan
        datetime(2024, 10, 12), # Dussehra
        datetime(2024, 11, 1),  # Diwali
        datetime(2024, 12, 25), # Christmas
    ]
    
    # Initialize data containers
    transactions = []
    
    for i in range(n_samples):
        # Generate transaction timestamp
        start_date = datetime(2024, 1, 1)
        days_offset = random.randint(0, 365)
        hour = np.random.choice(24, p=create_indian_hour_probability())
        transaction_time = start_date + timedelta(days=days_offset, hours=hour)
        
        # Determine fraud probability based on Indian patterns
        fraud_probability = calculate_indian_fraud_probability(
            transaction_time, hour, festivals
        )
        
        is_fraud = random.random() < fraud_probability
        
        # Select payment method
        if is_fraud:
            # Fraudsters prefer certain methods
            payment_method = np.random.choice(
                ['UPI', 'Net_Banking', 'Mobile_Banking', 'International_Card'],
                p=[0.4, 0.3, 0.2, 0.1]
            )
        else:
            payment_method = random.choice(payment_methods)
        
        # Select merchant category
        merchant = random.choice(indian_merchants)
        
        # Generate transaction amount based on Indian patterns
        amount = generate_indian_amount(merchant, is_fraud)
        
        # Select location
        if is_fraud and random.random() < 0.3:
            location = random.choice(suspicious_locations)
        else:
            location = random.choice(indian_locations)
        
        # Generate Indian-specific features
        features = generate_indian_features(
            payment_method, merchant, location, amount, 
            transaction_time, is_fraud
        )
        
        # Add transaction metadata
        transaction = {
            'Transaction_ID': f'TXN_{i+1:06d}',
            'Timestamp': transaction_time,
            'Amount': round(amount, 2),
            'Payment_Method': payment_method,
            'Merchant_Category': merchant,
            'Location': location,
            'Hour': transaction_time.hour,
            'Day_of_Week': transaction_time.weekday(),
            'Is_Festival_Season': is_near_festival(transaction_time, festivals),
            'Is_Banking_Hours': hour in banking_hours,
            'Is_Weekend': transaction_time.weekday() >= 5,
            'Month': transaction_time.month,
            'Class': 1 if is_fraud else 0
        }
        
        # Add anonymized features (V1-V28 like original dataset)
        transaction.update(features)
        
        transactions.append(transaction)
        
        if (i + 1) % 10000 == 0:
            print(f"Generated {i+1} transactions...")
    
    return pd.DataFrame(transactions)

def create_indian_hour_probability():
    """Indian transaction patterns - peak during business hours and evening"""
    probs = np.ones(24) * 0.02  # Base probability
    probs[9:17] = 0.08   # Business hours (heavy banking)
    probs[18:22] = 0.06  # Evening (UPI/online shopping)
    probs[12:14] = 0.04  # Lunch break (reduced)
    probs[0:6] = 0.01    # Night (very low)
    return probs / probs.sum()

def calculate_indian_fraud_probability(transaction_time, hour, festivals):
    """Calculate fraud probability based on Indian patterns"""
    base_fraud_rate = 0.025  # 2.5% base fraud rate
    
    # Night transactions (higher risk)
    if hour < 6 or hour > 23:
        base_fraud_rate *= 3
    
    # Weekend transactions
    if transaction_time.weekday() >= 5:
        base_fraud_rate *= 1.5
    
    # Festival season (higher fraud attempts)
    if is_near_festival(transaction_time, festivals):
        base_fraud_rate *= 2
    
    # End of month (salary time - more fraud)
    if transaction_time.day > 25:
        base_fraud_rate *= 1.3
    
    return min(base_fraud_rate, 0.15)  # Cap at 15%

def is_near_festival(date, festivals):
    """Check if date is within 7 days of any festival"""
    for festival in festivals:
        if abs((date - festival).days) <= 7:
            return True
    return False

def generate_indian_amount(merchant, is_fraud):
    """Generate realistic Indian transaction amounts"""
    if is_fraud:
        # Fraud patterns in India
        if random.random() < 0.4:
            return random.uniform(1, 100)  # Small test amounts
        else:
            return np.random.exponential(5000) + 1000  # Large fraud amounts
    
    # Normal transaction amounts by merchant type
    amount_patterns = {
        'Grocery_Kirana': lambda: np.random.gamma(2, 150),        # ₹300 average
        'Petrol_Pump': lambda: np.random.gamma(3, 200),          # ₹600 average
        'Mobile_Recharge': lambda: random.choice([199, 399, 599, 999]),
        'Electricity_Bill': lambda: np.random.gamma(2, 400),      # ₹800 average
        'E_Commerce': lambda: np.random.exponential(800) + 200,   # ₹1000 average
        'Gold_Jewellery': lambda: np.random.exponential(15000) + 5000,  # High value
        'Auto_Rickshaw': lambda: random.uniform(50, 300),      # ₹50-300
        'Train_Booking': lambda: random.choice([150, 300, 500, 1200, 2500]),
        'Movie_Ticket': lambda: random.choice([120, 180, 250, 350]),
        'DTH_Recharge': lambda: random.choice([199, 299, 499, 799]),
    }
    
    if merchant in amount_patterns:
        return amount_patterns[merchant]()
    else:
        return np.random.exponential(500) + 50

def generate_indian_features(payment_method, merchant, location, amount, time, is_fraud):
    """Generate Indian banking specific anonymized features"""
    features = {}
    
    # Generate V1-V28 features with Indian banking characteristics
    for i in range(1, 29):
        if is_fraud:
            # Fraudulent transactions have different patterns
            if i <= 10:  # Payment method related features
                if 'International' in location:
                    features[f'V{i}'] = np.random.normal(2.0, 1.5)
                else:
                    features[f'V{i}'] = np.random.normal(1.0, 1.2)
            elif i <= 20:  # Amount and time related features
                if amount > 10000:  # High value transactions
                    features[f'V{i}'] = np.random.normal(-1.5, 1.0)
                else:
                    features[f'V{i}'] = np.random.normal(0.5, 1.0)
            else:  # Location and behavioral features
                if time.hour < 6 or time.hour > 22:  # Night transactions
                    features[f'V{i}'] = np.random.normal(-2.0, 1.0)
                else:
                    features[f'V{i}'] = np.random.normal(0, 1.0)
        else:
            # Normal transactions
            features[f'V{i}'] = np.random.normal(0, 1.0)
    
    return features

if __name__ == "__main__":
    # Create Indian banking dataset
    print("🇮🇳 Creating Indian Banking Fraud Detection Dataset...")
    df = create_indian_banking_dataset(100000)
    
    # Save dataset
    df.to_csv('indian_banking_transactions.csv', index=False)
    
    print(f"\n✅ Created Indian banking dataset with {len(df)} transactions")
    print(f"📊 Fraud rate: {df['Class'].mean():.3%}")
    print(f"💰 Average transaction amount: ₹{df['Amount'].mean():.2f}")
    print(f"🚨 Fraud cases: {df['Class'].sum()}")
    
    print("\n📱 Payment Method Distribution:")
    print(df['Payment_Method'].value_counts())
    
    print("\n🏪 Top Merchant Categories:")
    print(df['Merchant_Category'].value_counts().head(10))
    
    print("\n🌍 Location Distribution:")
    print(df['Location'].value_counts().head(10))
    
    print("\n📈 Fraud by Payment Method:")
    fraud_by_method = df.groupby('Payment_Method')['Class'].agg(['count', 'sum', 'mean']).round(3)
    fraud_by_method.columns = ['Total', 'Fraud_Cases', 'Fraud_Rate']
    print(fraud_by_method.sort_values('Fraud_Rate', ascending=False))
    
    print("\n🎉 Sample transactions:")
    print(df[['Transaction_ID', 'Amount', 'Payment_Method', 'Merchant_Category', 'Location', 'Class']].head(10))
