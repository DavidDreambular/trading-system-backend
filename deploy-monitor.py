#!/usr/bin/env python3
"""
Deployment Monitor - Trading System
Monitorea el estado de deployment en tiempo real
"""

import requests
import time
import json
from datetime import datetime
import os

# URLs de servicios
SERVICES = {
    'AI Service': 'https://ai-service-production-dde4.up.railway.app/health',
    'Data Service': 'https://data-service-production-6f28.up.railway.app/health',
    'n8n': 'https://n8n-orchestrator-production.up.railway.app'
}

def check_service(name, url):
    """Verifica el estado de un servicio"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return "OK - ONLINE"
        else:
            return f"ERROR - HTTP {response.status_code}"
    except requests.exceptions.RequestException as e:
        return "ERROR - OFFLINE"

def main():
    """Monitor principal"""
    print("DEPLOYMENT MONITOR - TRADING SYSTEM")
    print("Press Ctrl+C to stop monitoring")
    
    try:
        iteration = 0
        while iteration < 5:  # Solo 5 iteraciones para no saturar
            iteration += 1
            
            print(f"\n--- CHECK #{iteration} ---")
            print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print()
            
            all_online = True
            
            for service_name, url in SERVICES.items():
                status = check_service(service_name, url)
                print(f"{service_name:<15}: {status}")
                
                if "ERROR" in status:
                    all_online = False
            
            print()
            
            if all_online:
                print(">>> ALL SERVICES OPERATIONAL!")
                print(">>> DEPLOYMENT SUCCESSFUL")
                break
            else:
                print(">>> Waiting for services to come online...")
                print(">>> Deployment in progress...")
            
            if iteration < 5:
                print("Next check in 15 seconds...")
                time.sleep(15)
                
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped by user")

if __name__ == "__main__":
    main()
