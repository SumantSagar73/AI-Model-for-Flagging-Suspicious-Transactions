"""
Create a synthetic credit card fraud dataset for testing purposes.
This replaces the need for Kaggle API credentials during development.
"""
import pandas as pd
import numpy as np

def create_synthetic_dataset():
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Create 10,000 transactions
    n_samples = 10000
    
    # Generate features (V1-V28 like in the real dataset)
    features = {}
    for i in range(1, 29):
        features[f'V{i}'] = np.random.normal(0, 1, n_samples)
    
    # Generate Time and Amount
    features['Time'] = np.random.randint(0, 172800, n_samples)  # 48 hours in seconds
    features['Amount'] = np.random.exponential(50, n_samples)  # Exponential distribution for amounts
    
    # Create DataFrame
    df = pd.DataFrame(features)
    
    # Generate fraud labels (5% fraud rate)
    df['Class'] = np.random.choice([0, 1], size=n_samples, p=[0.95, 0.05])
    
    # Make fraudulent transactions slightly different
    fraud_mask = df['Class'] == 1
    df.loc[fraud_mask, 'Amount'] *= 2  # Fraudulent transactions tend to be higher amounts
    
    # Save the dataset
    df.to_csv('creditcard.csv', index=False)
    print(f"Created synthetic dataset with {len(df)} transactions")
    print(f"Fraud rate: {df['Class'].mean():.2%}")
    print("Dataset saved as 'creditcard.csv'")

if __name__ == "__main__":
    create_synthetic_dataset()
