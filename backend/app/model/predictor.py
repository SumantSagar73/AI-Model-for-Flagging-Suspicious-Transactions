import joblib
import pandas as pd
import numpy as np
from backend.app.utils.preprocessing import preprocess_single, preprocess_batch

# Load Indian Banking model and preprocessors
MODEL_PATH = "backend/app/model/indian_banking_model.pkl"
SCALER_PATH = "backend/app/model/indian_banking_scaler.pkl"
FEATURE_COLUMNS_PATH = "backend/app/model/feature_columns.pkl"
PAYMENT_ENCODER_PATH = "backend/app/model/payment_encoder.pkl"
MERCHANT_ENCODER_PATH = "backend/app/model/merchant_encoder.pkl"
LOCATION_ENCODER_PATH = "backend/app/model/location_encoder.pkl"

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    feature_columns = joblib.load(FEATURE_COLUMNS_PATH)
    payment_encoder = joblib.load(PAYMENT_ENCODER_PATH)
    merchant_encoder = joblib.load(MERCHANT_ENCODER_PATH)
    location_encoder = joblib.load(LOCATION_ENCODER_PATH)
    print("Indian Banking model and preprocessors loaded successfully!")
except Exception as e:
    print(f"Error loading Indian Banking model: {e}")
    model = None
    scaler = None
    feature_columns = None
    payment_encoder = None
    merchant_encoder = None
    location_encoder = None

def preprocess_indian_banking_features(data):
    """
    Preprocess data for Indian Banking fraud detection model
    """
    if isinstance(data, dict):
        df = pd.DataFrame([data])
    else:
        df = data.copy()
    
    # Ensure required columns exist with defaults
    required_columns = ['Amount', 'Payment_Method', 'Merchant_Category', 'Location']
    for col in required_columns:
        if col not in df.columns:
            if col == 'Amount':
                df[col] = 1000.0  # Default amount
            elif col == 'Payment_Method':
                df[col] = 'UPI'  # Default to UPI
            elif col == 'Merchant_Category':
                df[col] = 'Others'  # Default category
            elif col == 'Location':
                df[col] = 'Mumbai'  # Default location
    
    # Create features similar to training
    df['Amount_Log'] = np.log1p(df['Amount'])
    
    # Encode categorical features
    try:
        df['Payment_Method_Encoded'] = payment_encoder.transform(df['Payment_Method'])
    except:
        df['Payment_Method_Encoded'] = 0  # Default encoding
    
    try:
        df['Merchant_Category_Encoded'] = merchant_encoder.transform(df['Merchant_Category'])
    except:
        df['Merchant_Category_Encoded'] = 0  # Default encoding
    
    try:
        df['Location_Encoded'] = location_encoder.transform(df['Location'])
    except:
        df['Location_Encoded'] = 0  # Default encoding
    
    # Create time-based features
    if 'Time' in df.columns:
        df['Hour'] = pd.to_datetime(df['Time']).dt.hour
    else:
        df['Hour'] = 12  # Default to noon
    
    # Create derived features
    df['Is_High_Risk_Payment'] = df['Payment_Method'].isin(['Card', 'Net Banking']).astype(int)
    df['Is_International'] = 0  # Default to domestic
    df['Is_Festival_Season'] = 0  # Default to non-festival
    df['Is_Night_Transaction'] = ((df['Hour'] >= 22) | (df['Hour'] <= 6)).astype(int)
    
    # Add dummy V features for compatibility with model
    for i in range(1, 29):
        if f'V{i}' not in df.columns:
            df[f'V{i}'] = np.random.normal(0, 1, len(df))
    
    # Select only the features used in training
    feature_cols = [col for col in feature_columns if col in df.columns]
    missing_cols = [col for col in feature_columns if col not in df.columns]
    
    # Add missing columns with default values
    for col in missing_cols:
        df[col] = 0
    
    # Return features in the same order as training
    return df[feature_columns]

def predict_single(data):
    if model is None or scaler is None:
        return {"error": "Model not loaded"}
    
    try:
        # Preprocess using Indian banking features
        X_df = preprocess_indian_banking_features(data)
        X_scaled = scaler.transform(X_df)
        
        prob = model.predict_proba(X_scaled)[0][1]
        label = prob > 0.5
        
        return {
            "is_fraud": bool(label),
            "probability": float(prob),
            "details": {
                "model": "Police AI Fraud Detection System",
                "timestamp": pd.Timestamp.now().isoformat(),
                "payment_method": data.get('Payment_Method', 'Unknown'),
                "amount": data.get('Amount', 0),
                "investigation_priority": "HIGH" if prob > 0.7 else "MEDIUM" if prob > 0.3 else "LOW",
                "recommendation": (
                    "Immediate investigation required - High fraud risk detected" if prob > 0.7 else
                    "Further verification recommended - Medium fraud risk" if prob > 0.3 else
                    "Routine processing - Low fraud risk"
                )
            }
        }
    except Exception as e:
        return {"error": f"Prediction failed: {str(e)}"}

def predict_batch(file):
    if model is None or scaler is None:
        return {"error": "Model not loaded"}
    
    try:
        df = pd.read_csv(file.file)
        X_df = preprocess_indian_banking_features(df)
        X_scaled = scaler.transform(X_df)
        
        probs = model.predict_proba(X_scaled)[:,1]
        labels = probs > 0.5
        
        results = [
            {
                "transaction_id": i+1,
                "is_fraud": bool(label),
                "probability": float(prob)
            }
            for i, (label, prob) in enumerate(zip(labels, probs))
        ]
        
        summary = {
            "total": len(results),
            "fraudulent": int(sum(labels)),
            "legit": len(results) - int(sum(labels))
        }
        
        return {"results": results, "summary": summary}
    except Exception as e:
        return {"error": f"Batch prediction failed: {str(e)}"}
