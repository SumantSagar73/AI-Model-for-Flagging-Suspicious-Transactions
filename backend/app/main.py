from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import pandas as pd
import asyncio
from datetime import datetime
from app.model.predictor import predict_single, predict_batch
from app.integrations.banking_api import IndianBankingAPIIntegrator
from app.analytics.advanced_analytics import AdvancedFinancialAnalytics

app = FastAPI(
    title="Police Financial Crime Investigation API",
    description="AI-powered fraud detection system for law enforcement agencies to analyze suspicious financial transactions",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TransactionRequest(BaseModel):
    Amount: float
    Payment_Method: Optional[str] = "UPI"
    Merchant_Category: Optional[str] = "Others"
    Location: Optional[str] = "Mumbai"
    Time: Optional[str] = None
    
    # Optional fields for backward compatibility
    V1: Optional[float] = None
    V2: Optional[float] = None
    V3: Optional[float] = None
    V4: Optional[float] = None
    V5: Optional[float] = None

@app.get("/")
def read_root():
    """Health check endpoint for police system"""
    return {
        "message": "Police Financial Crime Investigation API",
        "status": "active",
        "model": "AI Fraud Detection System for Law Enforcement",
        "department": "Cyber Crime Division",
        "jurisdiction": "Financial Crimes Unit"
    }

@app.post("/predict")
def predict_transaction(transaction: TransactionRequest):
    """
    Analyze suspicious financial transaction for law enforcement investigation
    
    Parameters:
    - Amount: Transaction amount in INR
    - Payment_Method: UPI, NEFT, RTGS, IMPS, Card, Net Banking
    - Merchant_Category: Retail, Food, Transport, Healthcare, etc.
    - Location: Indian city/state
    - Time: Transaction timestamp (optional)
    
    Returns: Risk assessment with investigation recommendations for police
    """
    data = transaction.dict()
    return predict_single(data)

@app.post("/predict_simple")
def predict_simple(data: dict):
    """Simple prediction endpoint for police case analysis (backward compatibility)"""
    return predict_single(data)

@app.post("/upload")
def upload_csv(file: UploadFile = File(...)):
    """
    Bulk case analysis via CSV upload for police investigation
    
    CSV should contain columns: Amount, Payment_Method, Merchant_Category, Location
    Returns: Risk assessment for all cases with investigation priorities
    """
    return predict_batch(file)

# Initialize integration modules
banking_integrator = IndianBankingAPIIntegrator()
analytics_engine = AdvancedFinancialAnalytics()

# New Banking API Integration Endpoints

@app.get("/banking/status")
async def banking_integration_status():
    """Check status of banking API integrations"""
    try:
        status = {}
        for bank_code in banking_integrator.connections.keys():
            auth_result = await banking_integrator.authenticate_bank(bank_code)
            status[bank_code] = {
                'name': banking_integrator.connections[bank_code].bank_name,
                'authenticated': auth_result.get('authenticated', False),
                'rate_limit': banking_integrator.connections[bank_code].rate_limit,
                'endpoints': banking_integrator.connections[bank_code].supported_endpoints
            }
        
        return {
            'banking_api_status': 'operational',
            'connected_banks': len(status),
            'bank_connections': status,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Banking API status check failed: {str(e)}")

@app.get("/banking/transactions/{bank_code}")
async def get_bank_transactions(
    bank_code: str,
    hours_back: Optional[int] = 1,
    min_amount: Optional[float] = None
):
    """Fetch real-time transactions from specific bank"""
    try:
        from_time = datetime.now() - pd.Timedelta(hours=hours_back)
        to_time = datetime.now()
        
        transactions_df = await banking_integrator.get_real_time_transactions(
            bank_code=bank_code,
            from_time=from_time,
            to_time=to_time,
            amount_threshold=min_amount
        )
        
        return {
            'bank_code': bank_code,
            'transaction_count': len(transactions_df),
            'time_range': {
                'from': from_time.isoformat(),
                'to': to_time.isoformat()
            },
            'transactions': transactions_df.to_dict('records')[:100],  # Limit to 100 for API response
            'summary': {
                'total_amount': transactions_df['amount'].sum(),
                'avg_amount': transactions_df['amount'].mean(),
                'max_amount': transactions_df['amount'].max(),
                'high_risk_count': len(transactions_df[transactions_df['amount'] > 500000])
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch transactions from {bank_code}: {str(e)}")

@app.post("/banking/alerts/{bank_code}")
async def setup_fraud_alerts(bank_code: str, alert_rules: Dict[str, Any]):
    """Setup real-time fraud alerts for specific bank"""
    try:
        alert_setup = await banking_integrator.setup_fraud_alerts(bank_code, alert_rules)
        return {
            'status': 'success',
            'alert_configuration': alert_setup,
            'message': f"Fraud alerts configured for {bank_code}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to setup alerts for {bank_code}: {str(e)}")

@app.get("/banking/account/{bank_code}/{account_number}")
async def investigate_account(bank_code: str, account_number: str):
    """Get detailed account information for investigation"""
    try:
        account_details = await banking_integrator.get_account_details(bank_code, account_number)
        return {
            'investigation_id': f"INV_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'account_details': account_details,
            'risk_assessment': {
                'overall_risk': account_details.get('risk_profile', 'unknown'),
                'kyc_status': 'verified' if account_details.get('kyc_details', {}).get('pan_verified') else 'unverified',
                'flags': account_details.get('flags', {}),
                'investigation_priority': 'HIGH' if account_details.get('flags', {}).get('suspicious_activity') else 'MEDIUM'
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Account investigation failed: {str(e)}")

# Advanced Analytics Endpoints

@app.post("/analytics/comprehensive")
async def comprehensive_analytics(file: UploadFile = File(...)):
    """Run comprehensive analytics on uploaded transaction data"""
    try:
        # Read uploaded CSV
        contents = await file.read()
        df = pd.read_csv(pd.io.common.StringIO(contents.decode('utf-8')))
        
        # Add timestamp if not present
        if 'timestamp' not in df.columns:
            df['timestamp'] = datetime.now()
        
        # Run comprehensive analysis
        results = analytics_engine.comprehensive_analysis_report(df)
        
        # Format results for API response
        formatted_results = {}
        for analysis_type, result in results.items():
            if analysis_type != 'executive_summary':
                formatted_results[analysis_type] = {
                    'summary': result.summary,
                    'risk_level': result.summary.get('risk_level', 'UNKNOWN'),
                    'recommendations': result.recommendations[:3],  # Top 3 recommendations
                    'key_findings': result.detailed_results
                }
        
        return {
            'analysis_id': f"ANALYTICS_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'executive_summary': results.get('executive_summary', {}),
            'analysis_results': formatted_results,
            'total_transactions': len(df),
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics processing failed: {str(e)}")

@app.post("/analytics/network")
async def network_analysis(file: UploadFile = File(...)):
    """Perform network analysis to identify suspect connections"""
    try:
        contents = await file.read()
        df = pd.read_csv(pd.io.common.StringIO(contents.decode('utf-8')))
        
        result = analytics_engine.network_analysis(df)
        
        return {
            'analysis_type': 'network_analysis',
            'summary': result.summary,
            'suspicious_entities': result.detailed_results.get('suspicious_nodes', [])[:10],
            'communities_detected': len(result.detailed_results.get('communities', [])),
            'recommendations': result.recommendations,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Network analysis failed: {str(e)}")

@app.post("/analytics/temporal")
async def temporal_analysis(file: UploadFile = File(...)):
    """Analyze temporal patterns in transaction data"""
    try:
        contents = await file.read()
        df = pd.read_csv(pd.io.common.StringIO(contents.decode('utf-8')))
        
        # Add timestamp if not present
        if 'timestamp' not in df.columns:
            df['timestamp'] = datetime.now()
        
        result = analytics_engine.temporal_pattern_analysis(df)
        
        return {
            'analysis_type': 'temporal_analysis',
            'summary': result.summary,
            'unusual_patterns': result.detailed_results.get('anomalies', []),
            'hourly_stats': result.detailed_results.get('hourly_stats', {}),
            'recommendations': result.recommendations,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Temporal analysis failed: {str(e)}")

@app.post("/analytics/geographic")
async def geographic_analysis(file: UploadFile = File(...)):
    """Analyze geographic patterns and clustering"""
    try:
        contents = await file.read()
        df = pd.read_csv(pd.io.common.StringIO(contents.decode('utf-8')))
        
        result = analytics_engine.geographic_clustering_analysis(df)
        
        return {
            'analysis_type': 'geographic_analysis',
            'summary': result.summary,
            'location_anomalies': result.detailed_results.get('geographic_anomalies', []),
            'high_risk_locations': result.detailed_results.get('high_risk_transactions', [])[:20],
            'recommendations': result.recommendations,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Geographic analysis failed: {str(e)}")

@app.post("/analytics/behavioral")
async def behavioral_analysis(file: UploadFile = File(...)):
    """Perform behavioral profiling analysis"""
    try:
        contents = await file.read()
        df = pd.read_csv(pd.io.common.StringIO(contents.decode('utf-8')))
        
        result = analytics_engine.behavioral_profiling(df)
        
        return {
            'analysis_type': 'behavioral_analysis',
            'summary': result.summary,
            'suspicious_customers': result.detailed_results.get('suspicious_customers', [])[:10],
            'behavioral_alerts': result.detailed_results.get('behavioral_alerts', []),
            'recommendations': result.recommendations,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Behavioral analysis failed: {str(e)}")

@app.post("/analytics/predictive")
async def predictive_modeling(file: UploadFile = File(...)):
    """Generate predictive risk scores and forecasts"""
    try:
        contents = await file.read()
        df = pd.read_csv(pd.io.common.StringIO(contents.decode('utf-8')))
        
        # Add timestamp if not present
        if 'timestamp' not in df.columns:
            df['timestamp'] = datetime.now()
        
        result = analytics_engine.predictive_risk_modeling(df)
        
        return {
            'analysis_type': 'predictive_modeling',
            'summary': result.summary,
            'high_risk_predictions': result.detailed_results.get('high_risk_transactions', [])[:20],
            'future_forecasts': result.detailed_results.get('future_predictions', []),
            'model_metrics': result.detailed_results.get('model_metrics', {}),
            'recommendations': result.recommendations,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Predictive modeling failed: {str(e)}")

# Multi-bank monitoring endpoint
@app.post("/banking/monitor/start")
async def start_multi_bank_monitoring(duration_minutes: int = 60):
    """Start monitoring all connected banks simultaneously"""
    try:
        
        async def alert_callback(alert_data):
            # In production, this would send to police dashboard/alert system
            print(f"🚨 FRAUD ALERT: {alert_data}")
        
        # Start monitoring task
        monitoring_task = asyncio.create_task(
            banking_integrator.monitor_all_banks(
                monitoring_duration=duration_minutes,
                alert_callback=alert_callback
            )
        )
        
        return {
            'status': 'monitoring_started',
            'duration_minutes': duration_minutes,
            'banks_monitored': list(banking_integrator.connections.keys()),
            'monitoring_id': f"MON_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'message': f"Real-time monitoring started for {duration_minutes} minutes across all banks"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start monitoring: {str(e)}")
