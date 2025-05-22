#!/usr/bin/env python3
"""
Integration Test Script for Trading System
Prueba la conectividad y funcionalidad básica de todos los servicios
"""

import requests
import json
import time
from datetime import datetime

# URLs de servicios
SERVICES = {
    'ai_service': 'https://ai-service-production-dde4.up.railway.app',
    'data_service': 'https://data-service-production-6f28.up.railway.app',
    'n8n': 'https://n8n-orchestrator-production.up.railway.app'
}

def test_service_health(service_name, url):
    """Prueba el health check de un servicio"""
    try:
        print(f"🔍 Testing {service_name} health...")
        response = requests.get(f"{url}/health", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {service_name}: {data.get('status', 'OK')}")
            return True
        else:
            print(f"❌ {service_name}: HTTP {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ {service_name}: Connection failed - {e}")
        return False

def main():
    """Ejecuta todos los tests de integración"""
    print("🚀 Trading System Integration Tests")
    print("=" * 50)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test health checks
    print(f"\n📋 HEALTH CHECKS")
    print("-" * 30)
    
    health_results = {}
    for service_name, url in SERVICES.items():
        health_results[service_name] = test_service_health(service_name, url)
    
    # Resumen
    print(f"\n📊 TEST SUMMARY")
    print("-" * 30)
    
    healthy_services = sum(health_results.values())
    total_services = len(health_results)
    
    print(f"✅ Healthy services: {healthy_services}/{total_services}")
    
    if healthy_services == total_services:
        print("🎉 All services are operational!")
    else:
        print("⚠️ Some services need attention")
        
    print(f"\n⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
