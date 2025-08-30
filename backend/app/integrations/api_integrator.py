"""
Comprehensive API Integration for Financial Crime Detection System
================================================================

This module provides integration with various financial crime detection APIs
and data sources that can be used alongside our local ML model.
"""

import requests
import json
import pandas as pd
from typing import Dict, List, Optional, Any
import asyncio
import aiohttp
from datetime import datetime, timedelta

class FinancialCrimeAPIIntegrator:
    """
    Integration class for various financial crime detection APIs
    """
    
    def __init__(self):
        # API endpoints (these would be real APIs in production)
        self.apis = {
            'fiu_india': {
                'base_url': 'https://api.fiu.gov.in/',
                'endpoints': {
                    'suspicious_reports': 'reports/suspicious',
                    'currency_reports': 'reports/currency',
                    'cross_border': 'reports/cross-border'
                }
            },
            'rbi_apis': {
                'base_url': 'https://api.rbi.org.in/',
                'endpoints': {
                    'blacklist_check': 'sanctions/check',
                    'kyc_verification': 'kyc/verify',
                    'aml_screening': 'aml/screen'
                }
            },
            'worldbank_sanctions': {
                'base_url': 'https://api.worldbank.org/sanctions/',
                'endpoints': {
                    'debarred_firms': 'firms/debarred',
                    'individual_sanctions': 'individuals/sanctioned'
                }
            },
            'ofac_sanctions': {
                'base_url': 'https://api.treasury.gov/ofac/',
                'endpoints': {
                    'sdn_list': 'sdn/search',
                    'consolidated_list': 'consolidated/search'
                }
            }
        }
    
    async def check_sanctions_lists(self, entity_name: str, entity_type: str = 'individual') -> Dict[str, Any]:
        """
        Check entity against multiple sanctions lists
        
        Args:
            entity_name: Name of individual or organization
            entity_type: 'individual' or 'organization'
            
        Returns:
            Dictionary with sanctions check results
        """
        results = {
            'entity_name': entity_name,
            'entity_type': entity_type,
            'sanctions_found': False,
            'sources': [],
            'risk_score': 0,
            'details': []
        }
        
        # Simulate API calls (in production, these would be real API calls)
        try:
            # OFAC SDN List check
            ofac_result = await self._check_ofac_sdn(entity_name)
            if ofac_result['match']:
                results['sanctions_found'] = True
                results['sources'].append('OFAC_SDN')
                results['risk_score'] += 90
                results['details'].append(ofac_result)
            
            # World Bank sanctions check
            wb_result = await self._check_worldbank_sanctions(entity_name, entity_type)
            if wb_result['match']:
                results['sanctions_found'] = True
                results['sources'].append('WORLD_BANK')
                results['risk_score'] += 85
                results['details'].append(wb_result)
            
            # RBI/FIU India check
            rbi_result = await self._check_rbi_sanctions(entity_name)
            if rbi_result['match']:
                results['sanctions_found'] = True
                results['sources'].append('RBI_INDIA')
                results['risk_score'] += 95
                results['details'].append(rbi_result)
                
        except Exception as e:
            results['error'] = str(e)
            
        return results
    
    async def _check_ofac_sdn(self, entity_name: str) -> Dict[str, Any]:
        """Simulate OFAC SDN list check"""
        # In production, this would make actual API call
        suspicious_names = ['terrorist', 'sanction', 'blocked', 'frozen']
        match = any(name.lower() in entity_name.lower() for name in suspicious_names)
        
        return {
            'source': 'OFAC_SDN',
            'match': match,
            'confidence': 0.85 if match else 0.0,
            'details': f"{'Match found' if match else 'No match'} in OFAC SDN database"
        }
    
    async def _check_worldbank_sanctions(self, entity_name: str, entity_type: str) -> Dict[str, Any]:
        """Simulate World Bank sanctions check"""
        suspicious_patterns = ['shell', 'offshore', 'laundering', 'fraud']
        match = any(pattern.lower() in entity_name.lower() for pattern in suspicious_patterns)
        
        return {
            'source': 'WORLD_BANK',
            'match': match,
            'confidence': 0.80 if match else 0.0,
            'details': f"{'Debarred entity found' if match else 'No match'} in World Bank database"
        }
    
    async def _check_rbi_sanctions(self, entity_name: str) -> Dict[str, Any]:
        """Simulate RBI/FIU India sanctions check"""
        indian_suspicious = ['hawala', 'benami', 'black money', 'terror funding']
        match = any(term.lower() in entity_name.lower() for term in indian_suspicious)
        
        return {
            'source': 'RBI_INDIA',
            'match': match,
            'confidence': 0.95 if match else 0.0,
            'details': f"{'Suspicious entity found' if match else 'Clean'} in Indian financial intelligence database"
        }
    
    def get_real_time_transaction_data(self, bank_code: str, date_range: int = 7) -> pd.DataFrame:
        """
        Simulate fetching real-time transaction data from banking APIs
        
        Args:
            bank_code: Bank identifier
            date_range: Number of days to fetch data for
            
        Returns:
            DataFrame with transaction data
        """
        # In production, this would connect to actual banking APIs
        # For now, we'll generate realistic sample data
        
        import random
        from datetime import datetime, timedelta
        
        transactions = []
        for i in range(random.randint(50, 200)):
            transaction = {
                'transaction_id': f"TXN_{bank_code}_{i:06d}",
                'amount': random.uniform(1000, 1000000),
                'payment_method': random.choice(['UPI', 'NEFT', 'RTGS', 'IMPS', 'Card']),
                'merchant_category': random.choice(['Retail', 'Food', 'Healthcare', 'Investment', 'Real_Estate']),
                'location': random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Pune']),
                'hour': random.randint(0, 23),
                'timestamp': datetime.now() - timedelta(days=random.randint(0, date_range))
            }
            transactions.append(transaction)
        
        return pd.DataFrame(transactions)
    
    def get_external_fraud_indicators(self, transaction_id: str) -> Dict[str, Any]:
        """
        Get fraud indicators from external sources
        
        Args:
            transaction_id: Unique transaction identifier
            
        Returns:
            Dictionary with external fraud indicators
        """
        # Simulate external fraud database lookup
        fraud_indicators = {
            'transaction_id': transaction_id,
            'external_flags': {
                'chargeback_history': random.choice([True, False]),
                'merchant_blacklist': random.choice([True, False]),
                'ip_reputation': random.uniform(0, 1),
                'device_fingerprint_risk': random.uniform(0, 1),
                'behavioral_anomaly': random.choice([True, False])
            },
            'risk_score': random.uniform(0, 100),
            'recommendation': 'INVESTIGATE' if random.random() > 0.7 else 'MONITOR'
        }
        
        return fraud_indicators

# Public APIs that can be used for fraud detection data
class PublicDataAPIs:
    """
    Integration with publicly available APIs for fraud detection
    """
    
    @staticmethod
    async def get_currency_exchange_rates(base_currency: str = 'INR') -> Dict[str, float]:
        """
        Get current exchange rates for detecting unusual currency conversions
        """
        # Using a free API like exchangerate-api.com
        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    data = await response.json()
                    return data.get('rates', {})
        except Exception as e:
            print(f"Error fetching exchange rates: {e}")
            return {}
    
    @staticmethod
    async def get_ip_geolocation(ip_address: str) -> Dict[str, Any]:
        """
        Get geolocation data for IP address to detect location anomalies
        """
        try:
            # Using a free API like ipapi.co
            url = f"https://ipapi.co/{ip_address}/json/"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.json()
        except Exception as e:
            print(f"Error fetching IP geolocation: {e}")
            return {}
    
    @staticmethod
    async def check_domain_reputation(domain: str) -> Dict[str, Any]:
        """
        Check domain reputation for merchant websites
        """
        # This would use services like VirusTotal, URLVoid, etc.
        # For demo purposes, returning simulated data
        return {
            'domain': domain,
            'reputation_score': random.uniform(0, 100),
            'malware_detected': random.choice([True, False]),
            'phishing_risk': random.uniform(0, 1),
            'age_days': random.randint(1, 3650)
        }

# Example usage and testing functions
async def test_api_integrations():
    """Test the API integrations"""
    api_integrator = FinancialCrimeAPIIntegrator()
    
    # Test sanctions check
    sanctions_result = await api_integrator.check_sanctions_lists("Suspicious Entity Ltd", "organization")
    print("Sanctions Check Result:", json.dumps(sanctions_result, indent=2))
    
    # Test real-time data fetch
    transaction_data = api_integrator.get_real_time_transaction_data("HDFC", 7)
    print(f"\nFetched {len(transaction_data)} transactions")
    print(transaction_data.head())
    
    # Test external fraud indicators
    fraud_indicators = api_integrator.get_external_fraud_indicators("TXN_123456")
    print("\nFraud Indicators:", json.dumps(fraud_indicators, indent=2))

if __name__ == "__main__":
    asyncio.run(test_api_integrations())
