from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import pandas as pd
import asyncio
import sys
import os
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our modules
from app.model.predictor import predict_single, predict_batch
from app.integrations.banking_api import IndianBankingAPIIntegrator
from app.analytics.advanced_analytics import AdvancedFinancialAnalytics

app = FastAPI(
    title="Police Financial Crime Investigation API",
    description="AI-powered fraud detection system for law enforcement agencies to analyze suspicious financial transactions with real banking integration and advanced analytics",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Transaction data model for police use
class TransactionData(BaseModel):
    Amount: float
    Payment_Method: str
    Merchant_Category: str
    Location: str

@app.get("/")
def read_root():
    """Welcome endpoint with system status"""
    return {
        "message": "🚔 Police Financial Crime Investigation API - Enhanced with Banking Integration & Analytics",
        "status": "operational",
        "version": "2.0.0",
        "features": [
            "🔍 AI-powered fraud detection",
            "🏦 Real banking API integration",
            "📊 Advanced analytics engine",
            "🚨 Real-time monitoring",
            "🌐 Network analysis",
            "📈 Predictive modeling"
        ],
        "available_endpoints": {
            "fraud_detection": ["/predict", "/upload"],
            "banking_integration": ["/banking/status", "/banking/transactions", "/banking/alerts"],
            "analytics": ["/analytics/comprehensive", "/analytics/network", "/analytics/temporal", "/analytics/geographic", "/analytics/behavioral", "/analytics/predictive"],
            "monitoring": ["/banking/monitor/start"]
        }
    }

@app.get("/health")
def health_check():
    """System health check for police operations center"""
    return {
        "status": "🟢 OPERATIONAL",
        "timestamp": datetime.now().isoformat(),
        "system": "Police Financial Crime Investigation API",
        "components": {
            "fraud_detection_model": "✅ Active",
            "banking_integration": "✅ Ready", 
            "analytics_engine": "✅ Operational",
            "real_time_monitoring": "✅ Standby"
        }
    }

@app.post("/predict")
def predict_transaction(data: TransactionData):
    """Single transaction fraud prediction for police case analysis"""
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

# Banking API Integration Endpoints

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
            'transactions': transactions_df.to_dict('records')[:100],
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
        contents = await file.read()
        df = pd.read_csv(pd.io.common.StringIO(contents.decode('utf-8')))
        
        if 'timestamp' not in df.columns:
            df['timestamp'] = datetime.now()
        
        results = analytics_engine.comprehensive_analysis_report(df)
        
        formatted_results = {}
        for analysis_type, result in results.items():
            if analysis_type != 'executive_summary':
                formatted_results[analysis_type] = {
                    'summary': result.summary,
                    'risk_level': result.summary.get('risk_level', 'UNKNOWN'),
                    'recommendations': result.recommendations[:3],
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

@app.post("/banking/monitor/start")
async def start_multi_bank_monitoring(duration_minutes: int = 60):
    """Start monitoring all connected banks simultaneously"""
    try:
        async def alert_callback(alert_data):
            print(f"🚨 FRAUD ALERT: {alert_data}")
        
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
