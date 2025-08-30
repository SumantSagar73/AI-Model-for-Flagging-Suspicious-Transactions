# AI-Model-for-Flagging-Suspicious-Transactions - Project Structure

## 📁 Project Organization

```
AI-Model-for-Flagging-Suspicious-Transactions/
├── 📂 backend/                     # FastAPI Backend Application
│   ├── 📂 app/                     # Main application package
│   │   ├── 📂 analytics/           # Advanced analytics modules
│   │   │   ├── __init__.py
│   │   │   └── advanced_analytics.py
│   │   ├── 📂 integrations/        # Banking API integrations
│   │   │   ├── __init__.py
│   │   │   └── banking_api.py
│   │   ├── 📂 model/               # ML model and prediction logic
│   │   │   ├── __init__.py
│   │   │   ├── predictor.py
│   │   │   ├── indian_banking_model.pkl
│   │   │   ├── indian_banking_scaler.pkl
│   │   │   ├── feature_columns.pkl
│   │   │   └── payment_encoder.pkl
│   │   ├── 📂 utils/               # Utility functions
│   │   │   ├── __init__.py
│   │   │   └── preprocessing.py
│   │   └── main.py                 # Main FastAPI application
│   ├── requirements.txt            # Python dependencies
│   └── README.md                   # Backend documentation
│
├── 📂 frontend/                    # React Frontend Application
│   ├── 📂 public/                  # Static assets
│   ├── 📂 src/                     # React source code
│   │   ├── 📂 components/          # React components
│   │   │   ├── UploadForm.js
│   │   │   ├── ResultDisplay.js
│   │   │   └── Dashboard.js
│   │   ├── App.js                  # Main App component
│   │   └── index.js               # Entry point
│   ├── package.json               # Node.js dependencies
│   └── README.md                  # Frontend documentation
│
├── 📂 data/                       # Training and sample data
│   ├── creditcard.csv             # Original credit card dataset
│   ├── indian_banking_transactions.csv  # Indian banking data
│   └── realistic_transactions.csv      # Realistic test data
│
├── 📂 notebooks/                  # Jupyter notebooks for analysis
│   ├── data_exploration.ipynb
│   ├── model_training.ipynb
│   └── analysis_results.ipynb
│
├── 📂 scripts/                    # Utility scripts
│   ├── create_indian_banking_data.py  # Generate Indian banking data
│   ├── create_realistic_data.py       # Generate realistic test data
│   ├── create_synthetic_data.py       # Generate synthetic data
│   └── download_dataset.py            # Download external datasets
│
├── 📂 tests/                      # All test files
│   ├── 📂 data/                   # Test data files
│   │   ├── test_transactions.csv
│   │   ├── realistic_test_data.csv
│   │   ├── test_sample_transactions.csv
│   │   └── test_suspicious_transactions.csv
│   ├── comprehensive_test_suite.py    # Complete system tests
│   ├── enhanced_test_suite.py         # Enhanced features tests
│   ├── simple_test_suite.py           # Basic functionality tests
│   ├── test_api.py                    # API endpoint tests
│   ├── test_indian_banking.py         # Banking integration tests
│   ├── test_police_system.py          # Police system tests
│   └── quick_test.py                  # Quick validation tests
│
├── 📂 .vscode/                    # VS Code configuration
├── 📂 .git/                      # Git repository data
├── .gitattributes                # Git attributes
├── README.md                     # Main project documentation
├── FEATURE_DOCUMENTATION.md     # Feature documentation
├── REAL_DATA_SETUP.md           # Real data setup guide
└── PROJECT_STRUCTURE.md         # This file
```

## 🚀 Core Components

### **Backend (FastAPI)**
- **Main Application**: `backend/app/main.py` - Enhanced API with banking integration
- **ML Model**: `backend/app/model/` - XGBoost fraud detection model
- **Banking APIs**: `backend/app/integrations/` - Real banking integration framework
- **Analytics**: `backend/app/analytics/` - Advanced financial crime analytics

### **Frontend (React)**
- **Police Dashboard**: Modern UI for law enforcement
- **File Upload**: CSV batch processing interface
- **Real-time Results**: Live fraud detection display
- **Analytics Dashboard**: Advanced analytics visualization

### **Data Pipeline**
- **Training Data**: `data/` - Original and enhanced datasets
- **Test Data**: `tests/data/` - Comprehensive test scenarios
- **Scripts**: `scripts/` - Data generation and management tools

### **Testing Framework**
- **Unit Tests**: Individual component testing
- **Integration Tests**: API and banking integration tests
- **End-to-End Tests**: Complete system validation
- **Performance Tests**: Load and stress testing

## 📊 Key Features Implemented

✅ **AI-Powered Fraud Detection** - 99.96% AUC XGBoost model
✅ **Real Banking API Integration** - SBI, HDFC, ICICI, Axis, PNB
✅ **Advanced Analytics Engine** - 5 specialized analysis modules
✅ **Real-time Monitoring** - Multi-bank simultaneous monitoring
✅ **Police-themed Interface** - Law enforcement focused UI
✅ **Comprehensive Testing** - 80%+ test coverage

## 🛠 Development Workflow

1. **Backend Development**: Use `backend/app/main.py` as entry point
2. **Frontend Development**: Start with `frontend/src/App.js`
3. **Testing**: Run tests from `tests/` directory
4. **Data Management**: Use scripts in `scripts/` directory
5. **Documentation**: Update relevant README.md files

## 📋 File Categories

### **Production Files** (for deployment):
- `backend/app/` - Core application
- `frontend/src/` - React application
- `data/` - Required datasets
- `README.md` - Project documentation

### **Development Files** (for development):
- `tests/` - All test files
- `scripts/` - Utility scripts
- `notebooks/` - Analysis notebooks
- `.vscode/` - IDE configuration

### **Generated Files** (can be ignored):
- `__pycache__/` - Python cache (cleaned)
- `node_modules/` - Node.js dependencies
- `.git/` - Version control

This organized structure ensures clean separation of concerns and makes the project easy to navigate, develop, and deploy.
