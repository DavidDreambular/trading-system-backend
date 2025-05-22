/**
 * Data Service - Servicio de Ingesta de Datos de Mercado
 * Obtiene datos de APIs externas: Alpha Vantage, NewsAPI, etc.
 */

const express = require('express');
const axios = require('axios');
const Redis = require('redis');
const cors = require('cors');
const rateLimit = require('express-rate-limit');

const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutos
  max: 100 // máximo 100 requests por ventana
});
app.use(limiter);

// Redis setup for caching
let redisClient;
if (process.env.REDIS_URL) {
  redisClient = Redis.createClient({
    url: process.env.REDIS_URL
  });
  redisClient.connect().catch(console.error);
} else {
  console.log('Redis not configured, running without cache');
}

// Configuration from environment variables
const config = {
  alphaVantage: {
    apiKey: process.env.ALPHA_VANTAGE_API_KEY,
    baseUrl: 'https://www.alphavantage.co/query'
  },
  newsApi: {
    apiKey: process.env.NEWS_API_KEY,
    baseUrl: 'https://newsapi.org/v2'
  },
  iex: {
    apiKey: process.env.IEX_API_KEY,
    baseUrl: 'https://cloud.iexapis.com/stable'
  }
};

// Utility functions
async function getCachedData(key, ttl = 300) {
  if (!redisClient) return null;
  
  try {
    const cached = await redisClient.get(key);
    return cached ? JSON.parse(cached) : null;
  } catch (error) {
    console.error('Redis get error:', error);
    return null;
  }
}

async function setCachedData(key, data, ttl = 300) {
  if (!redisClient) return;
  
  try {
    await redisClient.setEx(key, ttl, JSON.stringify(data));
  } catch (error) {
    console.error('Redis set error:', error);
  }
}

// Market Data Functions
async function getAlphaVantageData(symbol = 'AAPL', interval = '5min') {
  const cacheKey = `market_${symbol}_${interval}`;
  
  // Check cache first
  const cached = await getCachedData(cacheKey);
  if (cached) {
    console.log(`Returning cached data for ${symbol}`);
    return cached;
  }
  
  try {
    const url = `${config.alphaVantage.baseUrl}?function=TIME_SERIES_INTRADAY&symbol=${symbol}&interval=${interval}&apikey=${config.alphaVantage.apiKey}`;
    
    const response = await axios.get(url, {
      timeout: 10000
    });
    
    const data = response.data;
    const timeSeriesKey = `Time Series (${interval})`;
    
    if (data[timeSeriesKey]) {
      const timeSeries = data[timeSeriesKey];
      const timestamps = Object.keys(timeSeries).slice(0, 50);
      
      const formattedData = {
        ticker: symbol,
        prices: timestamps.map(ts => parseFloat(timeSeries[ts]['4. close'])),
        volumes: timestamps.map(ts => parseInt(timeSeries[ts]['5. volume'])),
        opens: timestamps.map(ts => parseFloat(timeSeries[ts]['1. open'])),
        highs: timestamps.map(ts => parseFloat(timeSeries[ts]['2. high'])),
        lows: timestamps.map(ts => parseFloat(timeSeries[ts]['3. low'])),
        timestamps: timestamps,
        lastUpdate: new Date().toISOString()
      };
      
      await setCachedData(cacheKey, formattedData, 300);
      return formattedData;
    } else {
      throw new Error('Invalid Alpha Vantage response format');
    }
    
  } catch (error) {
    console.error('Alpha Vantage API error:', error.message);
    
    // Return mock data as fallback
    return {
      ticker: symbol,
      prices: [150.0, 151.2, 149.8, 152.1, 151.0, 150.5],
      volumes: [1000000, 1100000, 950000, 1200000, 1050000, 1075000],
      opens: [149.5, 150.5, 151.0, 150.2, 151.8, 151.2],
      highs: [151.0, 152.0, 151.5, 152.5, 152.0, 151.8],
      lows: [149.0, 150.0, 149.5, 151.8, 150.5, 150.2],
      timestamps: [
        new Date(Date.now() - 25*60*1000).toISOString(),
        new Date(Date.now() - 20*60*1000).toISOString(),
        new Date(Date.now() - 15*60*1000).toISOString(),
        new Date(Date.now() - 10*60*1000).toISOString(),
        new Date(Date.now() - 5*60*1000).toISOString(),
        new Date().toISOString()
      ],
      lastUpdate: new Date().toISOString(),
      fallback: true
    };
  }
}

// API Routes
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'trading-data-service',
    timestamp: new Date().toISOString(),
    cache: redisClient ? 'enabled' : 'disabled'
  });
});

app.get('/market-data', async (req, res) => {
  try {
    const symbol = req.query.symbol || 'AAPL';
    const interval = req.query.interval || '5min';
    
    console.log(`Fetching market data for ${symbol} with ${interval} interval`);
    
    const data = await getAlphaVantageData(symbol, interval);
    
    res.json({
      success: true,
      data: data,
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    console.error('Market data endpoint error:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

app.get('/news', async (req, res) => {
  try {
    const query = req.query.q || 'stock market';
    const pageSize = parseInt(req.query.pageSize) || 20;
    
    console.log(`Fetching news for query: ${query}`);
    
    // Mock news data for now
    const data = {
      headlines: [
        "Stock Market Reaches New Highs Amid Economic Recovery",
        "Tech Stocks Continue Strong Performance in Q2",
        "Federal Reserve Maintains Interest Rates",
        "Energy Sector Shows Resilience Despite Global Concerns",
        "Retail Investors Drive Market Volatility"
      ],
      descriptions: [
        "Markets continue to show strong performance...",
        "Technology companies report better than expected earnings...",
        "The Federal Reserve decided to keep rates unchanged...",
        "Energy companies adapt to changing market conditions...",
        "Individual investors impact on market dynamics grows..."
      ],
      sources: ["Reuters", "Bloomberg", "CNBC", "MarketWatch", "Yahoo Finance"],
      timestamps: [
        new Date(Date.now() - 2*60*60*1000).toISOString(),
        new Date(Date.now() - 4*60*60*1000).toISOString(),
        new Date(Date.now() - 6*60*60*1000).toISOString(),
        new Date(Date.now() - 8*60*60*1000).toISOString(),
        new Date(Date.now() - 10*60*60*1000).toISOString()
      ],
      lastUpdate: new Date().toISOString(),
      totalResults: 5,
      fallback: true
    };
    
    res.json({
      success: true,
      data: data,
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    console.error('News endpoint error:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

app.listen(port, '0.0.0.0', () => {
  console.log(`Data service running on port ${port}`);
  console.log('Available endpoints:');
  console.log('  GET  /health');
  console.log('  GET  /market-data?symbol=AAPL&interval=5min');
  console.log('  GET  /news?q=stock market&pageSize=20');
});
