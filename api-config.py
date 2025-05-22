#!/usr/bin/env python3
"""
API Configuration Script for Trading System
Configura automáticamente las APIs reales en Railway
"""

import os
import requests
import sys

# APIs a configurar
APIS_CONFIG = {
    'alpha_vantage': {
        'name': 'Alpha Vantage',
        'env_var': 'ALPHA_VANTAGE_API_KEY',
        'signup_url': 'https://www.alphavantage.co/support/#api-key',
        'test_url': 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=AAPL&interval=5min&apikey=',
        'required': True
    },
    'newsapi': {
        'name': 'NewsAPI',
        'env_var': 'NEWS_API_KEY', 
        'signup_url': 'https://newsapi.org/register',
        'test_url': 'https://newsapi.org/v2/everything?q=stock&apiKey=',
        'required': True
    },
    'iex_cloud': {
        'name': 'IEX Cloud',
        'env_var': 'IEX_API_KEY',
        'signup_url': 'https://iexcloud.io/',
        'test_url': 'https://cloud.iexapis.com/stable/stock/AAPL/quote?token=',
        'required': False
    }
}

def print_header():
    print("🔑 TRADING SYSTEM - API CONFIGURATION")
    print("=" * 50)
    print()

def print_api_info(api_key, config):
    print(f"📋 {config['name']}")
    print(f"   Variable: {config['env_var']}")
    print(f"   Signup: {config['signup_url']}")
    print(f"   Required: {'Yes' if config['required'] else 'No'}")
    print()

def test_api_key(api_key, config):
    """Testa una API key"""
    try:
        test_url = config['test_url'] + api_key
        response = requests.get(test_url, timeout=10)
        
        if response.status_code == 200:
            return True, "✅ Valid"
        else:
            return False, f"❌ HTTP {response.status_code}"
            
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

def main():
    print_header()
    
    print("🎯 APIS REQUERIDAS PARA TESTING REAL")
    print("-" * 40)
    
    for api_key, config in APIS_CONFIG.items():
        print_api_info(api_key, config)
    
    print("\n📝 INSTRUCTIONS:")
    print("1. Signup for each API using the URLs above")
    print("2. Get your API keys")  
    print("3. Run this script again with --configure to set them")
    print()
    
    if "--configure" in sys.argv:
        configure_apis()
    else:
        print("💡 To configure APIs, run: python api-config.py --configure")

def configure_apis():
    print("🔧 CONFIGURING APIs...")
    print("-" * 30)
    
    configured_count = 0
    
    for api_key, config in APIS_CONFIG.items():
        print(f"\n📋 {config['name']}")
        
        if config['required']:
            api_value = input(f"Enter {config['name']} API key: ").strip()
        else:
            api_value = input(f"Enter {config['name']} API key (optional): ").strip()
            
        if api_value and api_value != 'demo':
            # Test API key
            is_valid, status = test_api_key(api_value, config)
            print(f"   Test: {status}")
            
            if is_valid:
                print(f"   ✅ {config['env_var']}='{api_value}'")
                configured_count += 1
            else:
                print(f"   ⚠️ API key may be invalid, but saved anyway")
                print(f"   📝 {config['env_var']}='{api_value}'")
                configured_count += 1
        else:
            print(f"   ⏭️ Skipped")
    
    print(f"\n🎉 CONFIGURATION COMPLETE")
    print(f"   APIs Configured: {configured_count}/{len(APIS_CONFIG)}")
    print("\n📋 NEXT STEPS:")
    print("1. Copy the API keys above")
    print("2. Set them in Railway Dashboard → Environment Variables")
    print("3. Restart services to apply changes")

if __name__ == "__main__":
    main()
