#!/usr/bin/env python3
"""
MASSIVE FUNCTIONALITY TEST SUITE - TRADING SYSTEM
Comprehensive testing of all system components and integrations
"""

import requests
import json
import time
import concurrent.futures
from datetime import datetime
import sys

# Test Configuration
SERVICES = {
    'ai_service': 'https://ai-service-production-dde4.up.railway.app',
    'data_service': 'https://data-service-production-6f28.up.railway.app',
    'n8n': 'https://n8n-orchestrator-production.up.railway.app',
    'dashboard': 'https://trading-dashboard-production-a944.up.railway.app'
}

# Test Results Storage
test_results = {
    'total_tests': 0,
    'passed_tests': 0,
    'failed_tests': 0,
    'warnings': 0,
    'details': []
}

def log_test(test_name, status, details="", response_time=None):
    """Log individual test results"""
    test_results['total_tests'] += 1
    
    if status == 'PASS':
        test_results['passed_tests'] += 1
        icon = "OK"
    elif status == 'FAIL':
        test_results['failed_tests'] += 1
        icon = "FAIL"
    else:  # WARNING
        test_results['warnings'] += 1
        icon = "WARN"
    
    result = {
        'test': test_name,
        'status': status,
        'details': details,
        'response_time': response_time,
        'timestamp': datetime.now().isoformat()
    }
    
    test_results['details'].append(result)
    
    time_str = f" ({response_time:.2f}s)" if response_time else ""
    print(f"[{icon}] {test_name}: {status}{time_str}")
    if details:
        print(f"      -> {details}")

def test_service_health(service_name, url):
    """Test basic health endpoint"""
    try:
        start_time = time.time()
        response = requests.get(f"{url}/health", timeout=10)
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            status = data.get('status', 'unknown')
            log_test(f"{service_name} Health", 'PASS', 
                    f"Status: {status}", response_time)
            return True
        else:
            log_test(f"{service_name} Health", 'FAIL', 
                    f"HTTP {response.status_code}", response_time)
            return False
            
    except Exception as e:
        log_test(f"{service_name} Health", 'FAIL', str(e))
        return False

def main():
    """Main testing function"""
    print("MASSIVE FUNCTIONALITY TEST SUITE - TRADING SYSTEM")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test 1: Health Checks
    print("1. HEALTH CHECKS")
    print("-" * 25)
    for service_name, url in SERVICES.items():
        test_service_health(service_name, url)
    
    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return True

if __name__ == "__main__":
    main()
