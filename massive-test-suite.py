#!/usr/bin/env python3
"""
MASSIVE FUNCTIONALITY TEST SUITE - TRADING SYSTEM
Comprehensive testing of all system components and integrations
"""

import requests
import json
import time
import asyncio
import aiohttp
from datetime import datetime
import sys
import os

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
        icon = "✅"
    elif status == 'FAIL':
        test_results['failed_tests'] += 1
        icon = "❌"
    else:  # WARNING
        test_results['warnings'] += 1
        icon = "⚠️"
    
    result = {
        'test': test_name,
        'status': status,
        'details': details,
        'response_time': response_time,
        'timestamp': datetime.now().isoformat()
    }
    
    test_results['details'].append(result)
    
    time_str = f" ({response_time:.2f}s)" if response_time else ""
    print(f"{icon} {test_name}: {status}{time_str}")
    if details:
        print(f"   └─ {details}")

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

def test_data_service_apis():
    """Test all Data Service endpoints"""
    base_url = SERVICES['data_service']
    
    # Test market data endpoint
    try:
        start_time = time.time()
        response = requests.get(f"{base_url}/market-data?symbol=AAPL", timeout=15)
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'prices' in data['data']:
                log_test("Data Service - Market Data", 'PASS', 
                        f"Retrieved {len(data['data']['prices'])} price points", response_time)
            else:
                log_test("Data Service - Market Data", 'WARNING', 
                        "Invalid data structure", response_time)
        else:
            log_test("Data Service - Market Data", 'FAIL', 
                    f"HTTP {response.status_code}", response_time)
    except Exception as e:
        log_test("Data Service - Market Data", 'FAIL', str(e))
    
    # Test news endpoint
    try:
        start_time = time.time()
        response = requests.get(f"{base_url}/news", timeout=15)
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'headlines' in data['data']:
                log_test("Data Service - News", 'PASS', 
                        f"Retrieved {len(data['data']['headlines'])} headlines", response_time)
            else:
                log_test("Data Service - News", 'WARNING', 
                        "Invalid data structure", response_time)
        else:
            log_test("Data Service - News", 'FAIL', 
                    f"HTTP {response.status_code}", response_time)
    except Exception as e:
        log_test("Data Service - News", 'FAIL', str(e))

def test_ai_service_analysis():
    """Test all AI Service analysis endpoints"""
    base_url = SERVICES['ai_service']
    
    # Test data for analysis
    market_data = {
        "market_data": {
            "prices": [150.0, 151.2, 149.8, 152.1, 151.0, 150.5],
            "volumes": [1000000, 1100000, 950000, 1200000, 1050000, 1075000]
        }
    }
    
    news_data = {
        "news_data": {
            "headlines": [
                "Stock market reaches new highs",
                "Tech stocks surge on earnings",
                "Economic growth shows positive trends"
            ]
        }
    }
    
    # Test technical analysis
    try:
        start_time = time.time()
        response = requests.post(f"{base_url}/analysis/technical", 
                               json=market_data, timeout=20)
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            if 'indicators' in data and 'rsi' in data['indicators']:
                log_test("AI Service - Technical Analysis", 'PASS', 
                        f"RSI: {data['indicators']['rsi']:.2f}", response_time)
            else:
                log_test("AI Service - Technical Analysis", 'WARNING', 
                        "Missing indicators", response_time)
        else:
            log_test("AI Service - Technical Analysis", 'FAIL', 
                    f"HTTP {response.status_code}", response_time)
    except Exception as e:
        log_test("AI Service - Technical Analysis", 'FAIL', str(e))
    
    # Test sentiment analysis
    try:
        start_time = time.time()
        response = requests.post(f"{base_url}/analysis/sentiment", 
                               json=news_data, timeout=20)
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            if 'sentiment' in data and 'sentiment_score' in data['sentiment']:
                score = data['sentiment']['sentiment_score']
                label = data['sentiment']['sentiment_label']
                log_test("AI Service - Sentiment Analysis", 'PASS', 
                        f"Score: {score:.3f} ({label})", response_time)
            else:
                log_test("AI Service - Sentiment Analysis", 'WARNING', 
                        "Missing sentiment data", response_time)
        else:
            log_test("AI Service - Sentiment Analysis", 'FAIL', 
                    f"HTTP {response.status_code}", response_time)
    except Exception as e:
        log_test("AI Service - Sentiment Analysis", 'FAIL', str(e))
    
    # Test fundamental analysis
    try:
        start_time = time.time()
        response = requests.post(f"{base_url}/analysis/fundamental", 
                               json=market_data, timeout=20)
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            if 'metrics' in data:
                log_test("AI Service - Fundamental Analysis", 'PASS', 
                        "Fundamental metrics generated", response_time)
            else:
                log_test("AI Service - Fundamental Analysis", 'WARNING', 
                        "Missing metrics", response_time)
        else:
            log_test("AI Service - Fundamental Analysis", 'FAIL', 
                    f"HTTP {response.status_code}", response_time)
    except Exception as e:
        log_test("AI Service - Fundamental Analysis", 'FAIL', str(e))

def test_integration_workflow():
    """Test complete integration workflow"""
    print("\n🔄 TESTING INTEGRATION WORKFLOW")
    
    # Step 1: Get market data
    try:
        data_response = requests.get(
            f"{SERVICES['data_service']}/market-data?symbol=AAPL", timeout=15)
        if data_response.status_code != 200:
            log_test("Integration - Market Data", 'FAIL', "Failed to get market data")
            return
        
        market_data = data_response.json()['data']
        log_test("Integration - Market Data", 'PASS', "Market data retrieved")
        
    except Exception as e:
        log_test("Integration - Market Data", 'FAIL', str(e))
        return
    
    # Step 2: Get news data
    try:
        news_response = requests.get(f"{SERVICES['data_service']}/news", timeout=15)
        if news_response.status_code != 200:
            log_test("Integration - News Data", 'FAIL', "Failed to get news data")
            return
        
        news_data = news_response.json()['data']
        log_test("Integration - News Data", 'PASS', "News data retrieved")
        
    except Exception as e:
        log_test("Integration - News Data", 'FAIL', str(e))
        return

    # Step 3: Run technical analysis
    try:
        tech_payload = {"market_data": {
            "prices": market_data['prices'],
            "volumes": market_data['volumes']
        }}
        
        tech_response = requests.post(
            f"{SERVICES['ai_service']}/analysis/technical", 
            json=tech_payload, timeout=20)
        
        if tech_response.status_code == 200:
            technical_analysis = tech_response.json()
            log_test("Integration - Technical Analysis", 'PASS', "Technical analysis completed")
        else:
            log_test("Integration - Technical Analysis", 'FAIL', 
                    f"HTTP {tech_response.status_code}")
            return
            
    except Exception as e:
        log_test("Integration - Technical Analysis", 'FAIL', str(e))
        return
    
    # Step 4: Run sentiment analysis
    try:
        sentiment_payload = {"news_data": {"headlines": news_data['headlines']}}
        
        sentiment_response = requests.post(
            f"{SERVICES['ai_service']}/analysis/sentiment", 
            json=sentiment_payload, timeout=20)
        
        if sentiment_response.status_code == 200:
            sentiment_analysis = sentiment_response.json()
            log_test("Integration - Sentiment Analysis", 'PASS', "Sentiment analysis completed")
        else:
            log_test("Integration - Sentiment Analysis", 'FAIL', 
                    f"HTTP {sentiment_response.status_code}")
            return
            
    except Exception as e:
        log_test("Integration - Sentiment Analysis", 'FAIL', str(e))
        return
    
    # Step 5: Generate trading signal
    try:
        fundamental_response = requests.post(
            f"{SERVICES['ai_service']}/analysis/fundamental", 
            json=tech_payload, timeout=20)
        
        if fundamental_response.status_code == 200:
            fundamental_analysis = fundamental_response.json()
            
            signal_payload = {
                "technical_analysis": technical_analysis,
                "fundamental_analysis": fundamental_analysis,
                "sentiment_analysis": sentiment_analysis
            }
            
            signal_response = requests.post(
                f"{SERVICES['ai_service']}/signal/generate", 
                json=signal_payload, timeout=20)
            
            if signal_response.status_code == 200:
                signal_data = signal_response.json()
                signal_type = signal_data.get('type', 'unknown')
                confidence = signal_data.get('confidence_score', 0)
                log_test("Integration - Signal Generation", 'PASS', 
                        f"Signal: {signal_type} (confidence: {confidence:.3f})")
            else:
                log_test("Integration - Signal Generation", 'FAIL', 
                        f"HTTP {signal_response.status_code}")
        else:
            log_test("Integration - Fundamental Analysis", 'FAIL', 
                    f"HTTP {fundamental_response.status_code}")
            
    except Exception as e:
        log_test("Integration - Signal Generation", 'FAIL', str(e))

def test_performance():
    """Test system performance under load"""
    print("\n⚡ TESTING PERFORMANCE")
    
    # Test concurrent requests to health endpoints
    import concurrent.futures
    
    def health_check_concurrent(service_info):
        service_name, url = service_info
        try:
            start_time = time.time()
            response = requests.get(f"{url}/health", timeout=5)
            response_time = time.time() - start_time
            return (service_name, response.status_code == 200, response_time)
        except:
            return (service_name, False, None)
    
    # Run concurrent health checks
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(health_check_concurrent, item) 
                  for item in SERVICES.items()]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    total_time = time.time() - start_time
    
    successful = sum(1 for _, success, _ in results if success)
    log_test("Performance - Concurrent Health Checks", 
            'PASS' if successful == len(SERVICES) else 'WARNING', 
            f"{successful}/{len(SERVICES)} services responding", total_time)

def main():
    """Main testing function"""
    print("🧪 MASSIVE FUNCTIONALITY TEST SUITE - TRADING SYSTEM")
    print("=" * 70)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test 1: Health Checks
    print("1️⃣ HEALTH CHECKS")
    print("-" * 30)
    for service_name, url in SERVICES.items():
        test_service_health(service_name, url)
    
    # Test 2: Data Service APIs
    print("\n2️⃣ DATA SERVICE APIs")
    print("-" * 30)
    test_data_service_apis()
    
    # Test 3: AI Service Analysis
    print("\n3️⃣ AI SERVICE ANALYSIS")
    print("-" * 30)
    test_ai_service_analysis()
    
    # Test 4: Integration Workflow
    test_integration_workflow()
    
    # Test 5: Performance
    test_performance()
    
    # Final Results
    print("\n" + "=" * 70)
    print("📊 FINAL TEST RESULTS")
    print("=" * 70)
    
    total = test_results['total_tests']
    passed = test_results['passed_tests']
    failed = test_results['failed_tests']
    warnings = test_results['warnings']
    
    print(f"✅ PASSED:   {passed}/{total} ({passed/total*100:.1f}%)")
    print(f"❌ FAILED:   {failed}/{total} ({failed/total*100:.1f}%)")
    print(f"⚠️ WARNINGS: {warnings}/{total} ({warnings/total*100:.1f}%)")
    
    success_rate = passed / total * 100
    if success_rate >= 90:
        print(f"\n🎉 EXCELLENT: {success_rate:.1f}% success rate!")
    elif success_rate >= 75:
        print(f"\n✅ GOOD: {success_rate:.1f}% success rate")
    else:
        print(f"\n⚠️ NEEDS ATTENTION: {success_rate:.1f}% success rate")
    
    print(f"\n⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Save detailed results
    with open('test_results.json', 'w') as f:
        json.dump(test_results, f, indent=2)
    
    return success_rate >= 75

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
