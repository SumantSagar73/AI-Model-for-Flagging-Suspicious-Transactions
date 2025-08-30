import pandas as pd
import numpy as np

def preprocess_single(df, scaler):
    """Preprocess a single transaction DataFrame"""
    # Select the feature columns (excluding Class if present)
    feature_cols = [col for col in df.columns if col != 'Class']
    
    # Handle missing values
    df_clean = df[feature_cols].fillna(0)
    
    # Scale the features
    X_scaled = scaler.transform(df_clean)
    
    return X_scaled[0]  # Return first row as 1D array

def preprocess_batch(df, scaler):
    """Preprocess a batch of transactions DataFrame"""
    # Select the feature columns (excluding Class if present)
    feature_cols = [col for col in df.columns if col != 'Class']
    
    # Handle missing values
    df_clean = df[feature_cols].fillna(0)
    
    # Scale the features
    X_scaled = scaler.transform(df_clean)
    
    return X_scaled
