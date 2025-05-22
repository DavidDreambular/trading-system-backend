# 🧪 POST-DEPLOYMENT VERIFICATION CHECKLIST

## ✅ SERVICES HEALTH CHECK

### AI Service Verification:
```bash
curl https://ai-service-production-dde4.up.railway.app/health
# Expected: {"status":"healthy","service":"trading-ai-service"}

curl https://ai-service-production-dde4.up.railway.app/market-data
# Expected: JSON with mock market data
```

### Data Service Verification:
```bash
curl https://data-service-production-6f28.up.railway.app/health
# Expected: {"status":"healthy","service":"trading-data-service"}

curl "https://data-service-production-6f28.up.railway.app/market-data?symbol=AAPL"
# Expected: JSON with market data (real or fallback)

curl "https://data-service-production-6f28.up.railway.app/news"
# Expected: JSON with news data
```

## 🔗 INTEGRATION TEST COMMANDS

### Complete Integration Test:
```bash
cd C:\projects\trading-system-backend
python scripts\integration-test.py
```

### Manual API Chain Test:
```bash
# 1. Get market data
curl "https://data-service-production-6f28.up.railway.app/market-data?symbol=AAPL" > market_data.json

# 2. Test technical analysis
curl -X POST https://ai-service-production-dde4.up.railway.app/analysis/technical \
  -H "Content-Type: application/json" \
  -d '{"market_data":{"prices":[150,151,149,152,151],"volumes":[1000000,1100000,950000,1200000,1050000]}}'

# 3. Test fundamental analysis  
curl -X POST https://ai-service-production-dde4.up.railway.app/analysis/fundamental \
  -H "Content-Type: application/json" \
  -d '{"market_data":{"prices":[150,151,149,152,151],"volumes":[1000000,1100000,950000,1200000,1050000]}}'

# 4. Test sentiment analysis
curl -X POST https://ai-service-production-dde4.up.railway.app/analysis/sentiment \
  -H "Content-Type: application/json" \
  -d '{"news_data":{"headlines":["Stock market rises","Tech stocks surge","Economy shows growth"]}}'
```

## 📊 SUCCESS METRICS

### Response Time Benchmarks:
- Health checks: < 2 seconds
- Market data API: < 5 seconds  
- AI analysis: < 10 seconds
- End-to-end workflow: < 30 seconds

### Expected Response Codes:
- All endpoints: 200 OK
- Health checks: JSON with status
- APIs: JSON with data or analysis

## 🎯 COMPLETION INDICATORS

✅ Both services show "Active" in Railway  
✅ Health endpoints return 200 OK  
✅ APIs return expected JSON responses  
✅ Integration test script passes  
✅ n8n workflow executes successfully  

**FINAL RESULT**: Fully functional trading system ready for production use.
