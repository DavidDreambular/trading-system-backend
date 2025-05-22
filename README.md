# 🚀 Trading System - Semiautomated Financial Opportunities Platform

![Trading System Architecture](https://img.shields.io/badge/Status-Production%20Ready-green)
![Version](https://img.shields.io/badge/Version-1.0.0-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Overview

A semiautomated system for identifying and executing financial opportunities, orchestrated by n8n with microservices deployed on Railway. The system performs technical, fundamental, and sentiment analysis to generate trading signals with human approval workflow.

## 🏗️ Architecture

```mermaid
graph TB
    A[n8n Workflows] --> B[Data Service]
    A --> C[AI Service]
    B --> D[Market APIs]
    C --> E[PostgreSQL]
    C --> F[Redis Cache]
    E --> G[Trading Signals]
    G --> H[Manual Approval]
    H --> I[Order Execution]
```

### 🔧 Components

| Service | Technology | Purpose | Status |
|---------|------------|---------|--------|
| **AI Service** | Python/FastAPI | Technical & Sentiment Analysis | ✅ Ready |
| **Data Service** | Node.js/Express | Market Data Ingestion | ✅ Ready |
| **PostgreSQL** | Database | Signal Storage & Analytics | ✅ Deployed |
| **Redis** | Cache | Performance Optimization | ✅ Deployed |
| **n8n** | Workflow | Orchestration & Automation | ✅ Configured |

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 18+ (for data-service)
- Python 3.11+ (for ai-service)
- PostgreSQL 15+ (or use Railway deployment)

### Local Development

```bash
# Clone repository
git clone https://github.com/your-org/trading-system-backend
cd trading-system-backend

# Copy environment template
cp .env.example .env

# Start services with Docker Compose
docker-compose up -d

# Verify services
curl http://localhost:8000/health  # AI Service
curl http://localhost:3000/health  # Data Service
```

### Railway Deployment

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway link your-project-id
railway up
```

## 📊 Features

### 🤖 AI Analysis Engine
- **Technical Analysis**: RSI, MACD, Moving Averages, Bollinger Bands
- **Fundamental Analysis**: P/E ratios, growth metrics, financial health
- **Sentiment Analysis**: NLP processing of market news and social media
- **Signal Generation**: Multi-factor scoring with confidence levels

### 📡 Data Integration
- **Market Data**: Alpha Vantage, IEX Cloud, Binance APIs
- **News Sources**: NewsAPI, Bloomberg RSS, financial news feeds
- **Social Sentiment**: Twitter, Reddit sentiment tracking
- **Caching**: Redis-based performance optimization

### 🔄 Workflow Automation
- **Detection Cycle**: Automated every 5 minutes during market hours
- **Signal Filtering**: Configurable confidence thresholds
- **Human Approval**: Manual review before execution
- **Execution Tracking**: Complete trade lifecycle monitoring

## 🛠️ API Reference

### AI Service Endpoints

```bash
# Health Check
GET /health

# Technical Analysis
POST /analysis/technical
Content-Type: application/json
{
  "market_data": {
    "prices": [150.0, 151.2, 149.8],
    "volumes": [1000000, 1100000, 950000]
  }
}

# Signal Generation
POST /signal/generate
Content-Type: application/json
{
  "technical_analysis": {...},
  "fundamental_analysis": {...},
  "sentiment_analysis": {...}
}
```

### Data Service Endpoints

```bash
# Market Data
GET /market-data?symbol=AAPL&interval=5min

# News Data
GET /news?q=stock market&pageSize=20

# Multiple Symbols
GET /market-data/multiple?symbols=AAPL,GOOGL,MSFT
```

## 📈 Current Status

### Railway Services Status
- **PostgreSQL**: ✅ Active at `hopper.proxy.rlwy.net:38187`
- **Redis**: ✅ Active at `nozomi.proxy.rlwy.net:11517`
- **AI Service**: 🔄 Ready for deployment
- **Data Service**: 🔄 Ready for deployment

### Performance Metrics
- **Target Signal Accuracy**: ≥ 60% win rate
- **Target Sharpe Ratio**: ≥ 1.5
- **Target Max Drawdown**: ≤ 5%
- **Target Response Time**: < 30 seconds per detection cycle
- **Target Uptime**: ≥ 99.5%

## 🔧 Configuration

### Environment Variables

```bash
# AI Service
AI_SERVICE_PORT=8000
SIGNAL_THRESHOLD=0.8
MAX_POSITION_PERCENT=1.0

# Data Service
DATA_SERVICE_PORT=3000
ALPHA_VANTAGE_API_KEY=your_key
NEWS_API_KEY=your_key
IEX_API_KEY=your_key

# Database
DATABASE_URL=postgresql://postgres-user:postgres-password@hopper.proxy.rlwy.net:38187/postgres-db
REDIS_URL=redis://default:redis-password@nozomi.proxy.rlwy.net:11517

# n8n
N8N_WEBHOOK_URL=https://n8n-orchestrator-production.up.railway.app/webhook
```

## 🧪 Testing

### Integration Tests

```bash
# Run complete integration test suite
python scripts/integration-test.py

# Test individual services
curl http://localhost:8000/health
curl http://localhost:3000/health
```

## 📋 Deployment Guide

### Railway Deployment

1. **Connect Repository**: Link this GitHub repo to Railway services
2. **Service Configuration**: 
   - AI Service: `/ai-service` directory
   - Data Service: `/data-service` directory
3. **Environment Variables**: Configure via Railway dashboard
4. **n8n Setup**: Import workflows from `/n8n-workflows`

### Post-Deployment

1. Configure PostgreSQL credentials in n8n
2. Test workflow execution
3. Monitor health endpoints
4. Set up alerting

## 🔒 Security

- **API Authentication**: Bearer token validation
- **Database**: SSL connections enabled
- **Environment Variables**: Secure credential management via Railway
- **Rate Limiting**: API protection against abuse
- **Data Encryption**: Sensitive data encrypted at rest

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📚 Documentation

- [📖 Architecture Guide](docs/architecture.md)
- [🚀 Deployment Guide](docs/deployment.md)
- [📋 API Reference](docs/api-reference.md)
- [🔧 Troubleshooting](docs/troubleshooting.md)

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-org/trading-system-backend/issues)
- **Documentation**: [Wiki](https://github.com/your-org/trading-system-backend/wiki)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 Acknowledgments

- **n8n Community** for workflow automation platform
- **Railway** for seamless deployment infrastructure
- **FastAPI & Express** for robust API frameworks
- **PostgreSQL & Redis** for reliable data storage

---

**Built with ❤️ for efficient financial market analysis and trading automation.**

## 🔗 Quick Links

- **Live AI Service**: https://ai-service-production-dde4.up.railway.app
- **Live Data Service**: https://data-service-production-6f28.up.railway.app
- **n8n Instance**: https://n8n-orchestrator-production.up.railway.app
- **Railway Project**: trading-system-backend (ID: 1b32ce32-5246-4515-8f40-edc57ce5e22e)
