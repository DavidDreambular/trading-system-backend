// Función real para NewsAPI - Agregar al server.js
async function getNewsAPIData(query = 'stock market', pageSize = 20) {
  const cacheKey = `news_${query}_${pageSize}`;
  
  // Check cache first
  const cached = await getCachedData(cacheKey, 600); // 10 min cache
  if (cached) {
    console.log(`Returning cached news for query: ${query}`);
    return cached;
  }
  
  try {
    // Skip if demo key
    if (config.newsApi.apiKey === 'demo') {
      throw new Error('Demo API key - using fallback');
    }
    
    const url = `${config.newsApi.baseUrl}/everything?q=${encodeURIComponent(query)}&apiKey=${config.newsApi.apiKey}&pageSize=${pageSize}&sortBy=publishedAt&language=en`;
    
    const response = await axios.get(url, {
      timeout: 10000
    });
    
    const articles = response.data.articles || [];
    
    const formattedData = {
      headlines: articles.map(article => article.title),
      descriptions: articles.map(article => article.description || ''),
      sources: articles.map(article => article.source?.name || 'Unknown'),
      urls: articles.map(article => article.url),
      timestamps: articles.map(article => article.publishedAt),
      lastUpdate: new Date().toISOString(),
      totalResults: response.data.totalResults || 0,
      fallback: false
    };
    
    await setCachedData(cacheKey, formattedData, 600);
    return formattedData;
    
  } catch (error) {
    console.error('NewsAPI error:', error.message);
    
    // Return enhanced mock data as fallback
    return {
      headlines: [
        "Stock Market Reaches New Highs Amid Economic Recovery",
        "Tech Stocks Continue Strong Performance in Q2", 
        "Federal Reserve Maintains Interest Rates",
        "Energy Sector Shows Resilience Despite Global Concerns",
        "Retail Investors Drive Market Volatility",
        `${query} Shows Mixed Trading Signals`,
        "Market Analysts Predict Continued Growth",
        "Banking Sector Outperforms Expectations"
      ],
      descriptions: [
        "Markets continue to show strong performance as economic indicators improve...",
        "Technology companies report better than expected earnings for the quarter...",
        "The Federal Reserve decided to keep rates unchanged citing current conditions...",
        "Energy companies adapt to changing market conditions and show resilience...",
        "Individual investors impact on market dynamics continues to grow...",
        `Analysis of ${query} reveals mixed signals from market participants...`,
        "Financial experts remain optimistic about market direction...",
        "Banking institutions report solid fundamentals and growth..."
      ],
      sources: ["Reuters", "Bloomberg", "CNBC", "MarketWatch", "Yahoo Finance", "Financial Times", "WSJ", "AP News"],
      urls: Array(8).fill("https://example.com/news"),
      timestamps: Array(8).fill(0).map((_, i) => new Date(Date.now() - (i+1)*2*60*60*1000).toISOString()),
      lastUpdate: new Date().toISOString(),
      totalResults: 8,
      fallback: true
    };
  }
}

// Actualizar endpoint /news para usar la función real
app.get('/news', async (req, res) => {
  try {
    const query = req.query.q || 'stock market';
    const pageSize = parseInt(req.query.pageSize) || 20;
    
    console.log(`Fetching news for query: ${query}`);
    
    const data = await getNewsAPIData(query, pageSize);
    
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
