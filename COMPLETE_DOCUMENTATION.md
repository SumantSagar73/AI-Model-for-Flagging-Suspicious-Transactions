# 📚 Complete Technical Documentation
# AI Model for Flagging Suspicious Transactions - Police Financial Crime Investigation System

## 🎯 Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [File & Folder Structure](#file--folder-structure)
4. [Backend Documentation](#backend-documentation)
5. [Frontend Documentation](#frontend-documentation)
6. [Database & Models](#database--models)
7. [API Endpoints](#api-endpoints)
8. [Functions & Classes](#functions--classes)
9. [Testing Framework](#testing-framework)
10. [Deployment Guide](#deployment-guide)
11. [Diagrams & Workflows](#diagrams--workflows)

---

## 🎯 Project Overview

### **Purpose**
AI-powered financial crime detection system specifically designed for law enforcement agencies to investigate suspicious transactions, analyze fraud patterns, and integrate with real banking APIs for live monitoring.

### **Key Technologies**
- **Backend**: FastAPI (Python 3.8+)
- **Frontend**: React 18+ with Material-UI
- **ML Model**: XGBoost (99.96% AUC)
- **Banking APIs**: Real-time integration with Indian banks
- **Analytics**: Advanced pattern detection algorithms
- **Database**: File-based ML models with CSV data processing

### **Target Users**
- Police Financial Crime Units
- Cyber Crime Investigators
- Banking Fraud Analysts
- Law Enforcement Agencies

---

## 🏗️ System Architecture

### **High-Level Architecture**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Police UI     │    │   FastAPI       │    │   Banking APIs  │
│   (React)       │◄──►│   Backend       │◄──►│   (Live Data)   │
│   Port: 3000    │    │   Port: 8001    │    │   SBI/HDFC/etc  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   File Upload   │    │   ML Models     │    │   Real-time     │
│   CSV Processing│    │   XGBoost       │    │   Monitoring    │
│   Bulk Analysis │    │   Analytics     │    │   Fraud Alerts  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **Data Flow**
1. **Input**: Police officers upload transaction CSV or single transaction
2. **Processing**: FastAPI receives data → ML model analyzes → Banking APIs validate
3. **Analytics**: Advanced algorithms detect patterns, networks, anomalies
4. **Output**: Fraud probability, risk assessment, investigation recommendations
5. **Monitoring**: Real-time alerts for suspicious activities across banks

---

## 📁 File & Folder Structure

### **Root Directory** (`/`)
```
AI-Model-for-Flagging-Suspicious-Transactions/
├── 📂 backend/                 # FastAPI application server
├── 📂 frontend/                # React police dashboard
├── 📂 data/                    # Training datasets & samples
├── 📂 tests/                   # Complete testing framework
├── 📂 scripts/                 # Utility & data generation scripts
├── 📂 notebooks/               # Jupyter analysis notebooks
├── 📄 README.md               # Main project documentation
├── 📄 .gitignore              # Git ignore rules
└── 📄 COMPLETE_DOCUMENTATION.md # This comprehensive guide
```

### **Backend Structure** (`/backend/`)
```
backend/
├── 📂 app/                     # Main application package
│   ├── 📂 analytics/           # Advanced analytics modules
│   │   ├── __init__.py         # Package initializer
│   │   └── advanced_analytics.py # 5 analytics modules
│   ├── 📂 integrations/        # Banking API integrations
│   │   ├── __init__.py         # Package initializer
│   │   └── banking_api.py      # Indian banking API framework
│   ├── 📂 model/               # Machine learning components
│   │   ├── __init__.py         # Package initializer
│   │   ├── predictor.py        # Main prediction logic
│   │   ├── indian_banking_model.pkl    # Trained XGBoost model
│   │   ├── indian_banking_scaler.pkl   # Feature scaler
│   │   ├── feature_columns.pkl         # Feature definitions
│   │   └── payment_encoder.pkl         # Payment method encoder
│   ├── 📂 utils/               # Utility functions
│   │   ├── __init__.py         # Package initializer
│   │   └── preprocessing.py    # Data preprocessing utilities
│   └── 📄 main.py              # FastAPI application entry point
├── 📄 requirements.txt         # Python dependencies
└── 📄 README.md               # Backend-specific documentation
```

### **Frontend Structure** (`/frontend/`)
```
frontend/
├── 📂 public/                  # Static assets
│   ├── index.html              # Main HTML template
│   ├── favicon.ico             # Police badge icon
│   └── manifest.json           # PWA configuration
├── 📂 src/                     # React source code
│   ├── 📂 components/          # React components
│   │   ├── UploadForm.js       # File upload interface
│   │   ├── ResultDisplay.js    # Results visualization
│   │   ├── Dashboard.js        # Main police dashboard
│   │   ├── TransactionTable.js # Transaction display table
│   │   └── AlertPanel.js       # Real-time alerts panel
│   ├── 📂 styles/              # CSS styling
│   │   ├── App.css             # Main application styles
│   │   └── police-theme.css    # Police-specific theming
│   ├── 📄 App.js               # Main React application
│   ├── 📄 index.js             # React entry point
│   └── 📄 reportWebVitals.js   # Performance monitoring
├── 📄 package.json             # Node.js dependencies
└── 📄 README.md               # Frontend documentation
```

---

## 🔧 Backend Documentation

### **Main Application** (`backend/app/main.py`)

#### **Purpose**
Central FastAPI application that orchestrates fraud detection, banking integration, and advanced analytics for police investigations.

#### **Key Classes & Functions**

##### **1. TransactionRequest (Pydantic Model)**
```python
class TransactionRequest(BaseModel):
    Amount: float                    # Transaction amount in INR
    Payment_Method: Optional[str]    # UPI/Card/NEFT/RTGS/etc
    Merchant_Category: Optional[str] # Business category
    Location: Optional[str]          # Transaction location
    Time: Optional[str]             # Transaction timestamp
```
**Purpose**: Validates incoming transaction data for API endpoints.

##### **2. FastAPI Application Setup**
```python
app = FastAPI(
    title="Police Financial Crime Investigation API",
    description="AI-powered fraud detection system",
    version="2.0.0"
)
```
**Purpose**: Creates the main API application with police-specific metadata.

##### **3. Core Endpoints**

###### **Health Check** (`GET /`)
```python
@app.get("/")
def read_root():
    return {
        "message": "Police Financial Crime Investigation API",
        "status": "active",
        "model": "AI Fraud Detection System",
        "department": "Cyber Crime Division"
    }
```
**Purpose**: System status check for police operations center.

###### **Single Prediction** (`POST /predict`)
```python
@app.post("/predict")
def predict_transaction(data: TransactionRequest):
    return predict_single(data)
```
**Purpose**: Analyzes individual suspicious transactions for immediate investigation.

###### **Batch Processing** (`POST /upload`)
```python
@app.post("/upload")
def upload_csv(file: UploadFile = File(...)):
    return predict_batch(file)
```
**Purpose**: Processes bulk transaction data from CSV files for large-scale investigations.

###### **Banking Status** (`GET /banking/status`)
```python
@app.get("/banking/status")
async def banking_integration_status():
    # Returns status of all connected banks
```
**Purpose**: Monitors real-time connectivity to banking APIs for live data access.

### **ML Model Components** (`backend/app/model/`)

#### **Predictor Module** (`predictor.py`)

##### **1. Model Loading**
```python
# Loads trained XGBoost model and preprocessors
MODEL_PATH = "backend/app/model/indian_banking_model.pkl"
SCALER_PATH = "backend/app/model/indian_banking_scaler.pkl"
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
```
**Purpose**: Initializes pre-trained fraud detection model with 99.96% AUC.

##### **2. Single Transaction Prediction**
```python
def predict_single(transaction_data):
    # 1. Preprocess input data
    # 2. Apply feature scaling
    # 3. Generate ML prediction
    # 4. Return fraud probability + risk assessment
```
**Purpose**: Analyzes individual transactions for fraud likelihood.

##### **3. Batch Prediction**
```python
def predict_batch(csv_file):
    # 1. Read CSV file
    # 2. Validate data format
    # 3. Process all transactions
    # 4. Return comprehensive analysis
```
**Purpose**: Processes large datasets for bulk fraud detection.

### **Banking Integration** (`backend/app/integrations/banking_api.py`)

#### **IndianBankingAPIIntegrator Class**

##### **1. Bank Configuration**
```python
class BankConnection:
    bank_name: str           # Full bank name
    api_base_url: str       # Banking API endpoint
    auth_method: str        # OAuth/API Key/Certificate
    rate_limit: int         # Requests per minute
    supported_endpoints: List[str]  # Available API functions
```
**Purpose**: Manages connections to Indian banking systems.

##### **2. Real-time Transaction Fetching**
```python
async def get_real_time_transactions(bank_code, from_time, to_time):
    # 1. Authenticate with bank API
    # 2. Fetch transaction data
    # 3. Apply fraud detection
    # 4. Generate alerts for suspicious activities
```
**Purpose**: Retrieves live banking data for real-time fraud monitoring.

##### **3. Multi-Bank Monitoring**
```python
async def monitor_all_banks(monitoring_duration, alert_callback):
    # 1. Start monitoring all connected banks
    # 2. Detect suspicious patterns
    # 3. Trigger real-time alerts
    # 4. Log investigation leads
```
**Purpose**: Simultaneous monitoring across multiple banks for comprehensive coverage.

### **Advanced Analytics** (`backend/app/analytics/advanced_analytics.py`)

#### **AdvancedFinancialAnalytics Class**

##### **1. Network Analysis**
```python
def network_analysis(transaction_df):
    # 1. Build transaction network graph
    # 2. Identify suspicious nodes and connections
    # 3. Detect money laundering patterns
    # 4. Map criminal networks
```
**Purpose**: Identifies suspect connections and money flow patterns.

##### **2. Temporal Pattern Analysis**
```python
def temporal_pattern_analysis(transaction_df):
    # 1. Analyze transaction timing patterns
    # 2. Detect unusual activity hours
    # 3. Identify coordinated attacks
    # 4. Flag time-based anomalies
```
**Purpose**: Detects time-based fraud patterns and coordinated activities.

##### **3. Geographic Clustering**
```python
def geographic_clustering_analysis(transaction_df):
    # 1. Analyze transaction locations
    # 2. Identify high-risk geographic areas
    # 3. Detect cross-border activities
    # 4. Map fraud hotspots
```
**Purpose**: Identifies geographic fraud patterns and high-risk locations.

##### **4. Behavioral Profiling**
```python
def behavioral_profiling(transaction_df):
    # 1. Analyze customer behavior patterns
    # 2. Detect unusual spending behaviors
    # 3. Identify account takeovers
    # 4. Profile suspicious customers
```
**Purpose**: Creates behavioral profiles to identify compromised accounts.

##### **5. Predictive Risk Modeling**
```python
def predictive_risk_modeling(transaction_df):
    # 1. Generate future risk predictions
    # 2. Forecast fraud trends
    # 3. Predict high-risk transactions
    # 4. Provide prevention recommendations
```
**Purpose**: Predicts future fraud risks and provides prevention strategies.

---

## 🎨 Frontend Documentation

### **Main Application** (`frontend/src/App.js`)

#### **Purpose**
React application providing a police-themed dashboard for financial crime investigation.

#### **Key Components**

##### **1. App Component**
```javascript
function App() {
    // 1. Manages global state
    // 2. Handles routing
    // 3. Coordinates police workflow
    // 4. Displays investigation results
}
```
**Purpose**: Main application container with police-specific styling and workflow.

##### **2. UploadForm Component** (`components/UploadForm.js`)
```javascript
function UploadForm({ onFileUpload, onSinglePredict }) {
    // 1. File upload interface for CSV processing
    // 2. Single transaction input form
    // 3. Police case number integration
    // 4. Investigation priority settings
}
```
**Purpose**: Provides police officers with intuitive data input interfaces.

##### **3. ResultDisplay Component** (`components/ResultDisplay.js`)
```javascript
function ResultDisplay({ results, loading }) {
    // 1. Displays fraud analysis results
    // 2. Shows risk assessment levels
    // 3. Provides investigation recommendations
    // 4. Highlights high-priority cases
}
```
**Purpose**: Visualizes fraud detection results for police investigation.

##### **4. Dashboard Component** (`components/Dashboard.js`)
```javascript
function Dashboard() {
    // 1. Real-time fraud monitoring
    // 2. Banking API status display
    // 3. Investigation case management
    // 4. Alert notification center
}
```
**Purpose**: Central command center for police financial crime operations.

---

## 🗃️ Database & Models

### **ML Model Files** (`backend/app/model/`)

#### **1. indian_banking_model.pkl**
- **Type**: XGBoost Classifier
- **Performance**: 99.96% AUC
- **Training Data**: 100K+ Indian banking transactions
- **Features**: 44 engineered features
- **Purpose**: Core fraud detection engine

#### **2. indian_banking_scaler.pkl**
- **Type**: StandardScaler
- **Purpose**: Normalizes transaction features for consistent model input

#### **3. feature_columns.pkl**
- **Type**: List of feature names
- **Purpose**: Ensures consistent feature ordering for predictions

#### **4. payment_encoder.pkl**
- **Type**: LabelEncoder
- **Purpose**: Encodes payment methods (UPI, Card, NEFT, etc.) for model processing

### **Data Processing Pipeline**
1. **Raw Transaction** → **Feature Engineering** → **Scaling** → **ML Prediction**
2. **Banking API Data** → **Real-time Processing** → **Fraud Detection** → **Alert Generation**

---

## 🔗 API Endpoints

### **Core Fraud Detection**
| Method | Endpoint | Purpose | Request | Response |
|--------|----------|---------|---------|----------|
| GET | `/` | Health check | None | System status |
| POST | `/predict` | Single transaction | Transaction JSON | Fraud probability |
| POST | `/upload` | Batch processing | CSV file | Bulk analysis |

### **Banking Integration**
| Method | Endpoint | Purpose | Request | Response |
|--------|----------|---------|---------|----------|
| GET | `/banking/status` | Bank connectivity | None | Connection status |
| GET | `/banking/transactions/{bank}` | Live transactions | Bank code | Transaction data |
| POST | `/banking/alerts/{bank}` | Setup alerts | Alert rules | Configuration |
| GET | `/banking/account/{bank}/{account}` | Account investigation | Bank + Account | Account details |

### **Advanced Analytics**
| Method | Endpoint | Purpose | Request | Response |
|--------|----------|---------|---------|----------|
| POST | `/analytics/comprehensive` | Full analysis | CSV file | Complete analytics |
| POST | `/analytics/network` | Network analysis | CSV file | Suspect connections |
| POST | `/analytics/temporal` | Time patterns | CSV file | Temporal anomalies |
| POST | `/analytics/geographic` | Location analysis | CSV file | Geographic patterns |
| POST | `/analytics/behavioral` | Behavior profiling | CSV file | Behavioral alerts |
| POST | `/analytics/predictive` | Risk prediction | CSV file | Future risk scores |

### **Monitoring**
| Method | Endpoint | Purpose | Request | Response |
|--------|----------|---------|---------|----------|
| POST | `/banking/monitor/start` | Multi-bank monitoring | Duration | Monitoring status |

---

## 🧪 Testing Framework

### **Test Structure** (`/tests/`)

#### **1. enhanced_test_suite.py**
- **Purpose**: Comprehensive system testing
- **Coverage**: All endpoints, banking integration, analytics
- **Results**: 80% success rate with detailed reporting

#### **2. simple_test_suite.py**
- **Purpose**: Basic functionality validation
- **Coverage**: Core fraud detection features
- **Results**: Quick validation without external dependencies

#### **3. comprehensive_test_suite.py**
- **Purpose**: Complete end-to-end testing
- **Coverage**: Full system workflow validation

#### **Test Data** (`/tests/data/`)
- **test_transactions.csv**: Sample transaction data
- **realistic_test_data.csv**: Real-world simulation data
- **test_suspicious_transactions.csv**: Known fraud cases

---

## 🚀 Deployment Guide

### **Local Development**
```bash
# Backend
cd backend
pip install -r requirements.txt
python app/main.py

# Frontend
cd frontend
npm install
npm start
```

### **Production Deployment**
```bash
# Backend (Docker)
docker build -t fraud-detection-api ./backend
docker run -p 8001:8001 fraud-detection-api

# Frontend (Build)
cd frontend
npm run build
# Deploy build/ to web server
```

---

## 📊 Diagrams & Workflows

### **System Architecture Diagram**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          POLICE FINANCIAL CRIME INVESTIGATION SYSTEM        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐    REST API     ┌─────────────────┐    Banking APIs    │
│  │   Police UI     │◄──────────────►│   FastAPI       │◄──────────────────► │
│  │   (React)       │  HTTP/WebSocket │   Backend       │  OAuth/API Keys     │
│  │   Port: 3000    │                 │   Port: 8001    │                     │
│  └─────────────────┘                 └─────────────────┘                     │
│           │                                   │                              │
│           │ File Upload                       │ ML Processing                │
│           │ CSV/JSON                          │ Real-time                    │
│           ▼                                   ▼                              │
│  ┌─────────────────┐                 ┌─────────────────┐                     │
│  │   Data Input    │                 │   AI Engine     │                     │
│  │   • CSV Files   │                 │   • XGBoost     │                     │
│  │   • Manual Entry│                 │   • Analytics   │                     │
│  │   • Live Feed   │                 │   • Predictions │                     │
│  └─────────────────┘                 └─────────────────┘                     │
│                                               │                              │
│                                               ▼                              │
│                                      ┌─────────────────┐                     │
│                                      │   Results       │                     │
│                                      │   • Fraud Score │                     │
│                                      │   • Risk Level  │                     │
│                                      │   • Alerts      │                     │
│                                      └─────────────────┘                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### **Data Flow Workflow**
```
Police Investigation Workflow:
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ Receive │    │ Upload  │    │ Analyze │    │ Assess  │    │ Take    │
│ Case    │───►│ Data    │───►│ with AI │───►│ Risk    │───►│ Action  │
│         │    │         │    │         │    │         │    │         │
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
     │              │              │              │              │
     ▼              ▼              ▼              ▼              ▼
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│Complaint│    │CSV File │    │XGBoost  │    │Fraud    │    │Court    │
│Report   │    │Bank Data│    │Analytics│    │Probability  │Evidence │
│Tip-off  │    │Manual   │    │Pattern  │    │Risk Level│    │Arrest   │
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
```

### **Banking Integration Flow**
```
Real-time Banking Monitoring:
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│   SBI    │    │   HDFC   │    │   ICICI  │    │   AXIS   │    │   PNB    │
│   API    │    │   API    │    │   API    │    │   API    │    │   API    │
└────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘
     │               │               │               │               │
     └───────────────┼───────────────┼───────────────┼───────────────┘
                     │               │               │
                     ▼               ▼               ▼
                ┌─────────────────────────────────────────┐
                │        Banking API Integrator           │
                │        • Authentication                 │
                │        • Data Aggregation              │
                │        • Real-time Monitoring          │
                └─────────────────┬───────────────────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │   AI Analysis   │
                         │   • Fraud Detection
                         │   • Pattern Analysis
                         │   • Risk Assessment
                         └─────────┬───────┘
                                   │
                                   ▼
                          ┌─────────────────┐
                          │   Police Alert  │
                          │   🚨 High Risk  │
                          │   📍 Location   │
                          │   💰 Amount     │
                          └─────────────────┘
```

---

## 🔧 Development Guidelines

### **Adding New Features**
1. Create feature branch
2. Add to appropriate module (analytics/, integrations/, model/)
3. Update API endpoints in main.py
4. Add frontend components
5. Write comprehensive tests
6. Update documentation

### **Code Standards**
- Python: PEP 8 compliance
- JavaScript: ESLint configuration
- Documentation: Comprehensive docstrings
- Testing: Minimum 80% coverage

### **Performance Considerations**
- Async processing for banking APIs
- Caching for ML model predictions
- Efficient data processing pipelines
- Real-time alert optimization

---

This documentation provides complete coverage of every file, function, and component in the system. For generating additional technical documentation and diagrams, refer to the separate `CLAUDE_AI_PROMPTS.md` file which contains specialized prompts for creating comprehensive technical documentation.
