"""
Trading AI Service - Microservicio de Análisis de Trading
Análisis técnico, fundamental, sentimiento y generación de señales
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import httpx
import asyncio
from textblob import TextBlob
import ta

app = FastAPI(title="Trading AI Service", version="1.0.0")

# Modelos de datos
class MarketData(BaseModel):
    ticker: str
    prices: List[float]
    volumes: List[float]
    timestamps: List[str]

class NewsData(BaseModel):
    headlines: List[str]
    sources: List[str]
    timestamps: List[str]

class TechnicalAnalysisRequest(BaseModel):
    market_data: Dict[str, Any]

class FundamentalAnalysisRequest(BaseModel):
    market_data: Dict[str, Any]

class SentimentAnalysisRequest(BaseModel):
    news_data: Dict[str, Any]

class SignalGenerationRequest(BaseModel):
    technical_analysis: Dict[str, Any]
    fundamental_analysis: Dict[str, Any]
    sentiment_analysis: Dict[str, Any]

class TradingSignal(BaseModel):
    ticker: str
    type: str  # buy, sell, hold
    size: float
    confidence_score: float
    reason: str
    created_at: datetime

# Funciones de análisis técnico
def calculate_technical_indicators(prices: List[float], volumes: List[float]) -> Dict[str, Any]:
    """Calcula indicadores técnicos básicos"""
    df = pd.DataFrame({
        'close': prices,
        'volume': volumes
    })
    
    # Moving Averages
    df['ma_short'] = df['close'].rolling(window=10).mean()
    df['ma_long'] = df['close'].rolling(window=30).mean()
    
    # RSI
    df['rsi'] = ta.momentum.RSIIndicator(close=df['close']).rsi()
    
    # MACD
    macd_indicator = ta.trend.MACD(close=df['close'])
    df['macd'] = macd_indicator.macd()
    df['macd_signal'] = macd_indicator.macd_signal()
    df['macd_histogram'] = macd_indicator.macd_diff()
    
    # Bollinger Bands
    bb_indicator = ta.volatility.BollingerBands(close=df['close'])
    df['bb_upper'] = bb_indicator.bollinger_hband()
    df['bb_lower'] = bb_indicator.bollinger_lband()
    df['bb_middle'] = bb_indicator.bollinger_mavg()
    
    latest = df.iloc[-1]
    
    return {
        'ma_crossover': float(latest['ma_short'] - latest['ma_long']),
        'rsi': float(latest['rsi']),
        'macd': float(latest['macd']),
        'macd_signal': float(latest['macd_signal']),
        'macd_histogram': float(latest['macd_histogram']),
        'price_vs_bb_upper': float(latest['close'] - latest['bb_upper']) / latest['close'],
        'price_vs_bb_lower': float(latest['close'] - latest['bb_lower']) / latest['close'],
        'current_price': float(latest['close']),
        'ma_short': float(latest['ma_short']),
        'ma_long': float(latest['ma_long'])
    }

def analyze_sentiment(headlines: List[str]) -> Dict[str, Any]:
    """Analiza el sentimiento de las noticias"""
    if not headlines:
        return {'sentiment_score': 0.0, 'sentiment_label': 'neutral'}
    
    sentiments = []
    for headline in headlines:
        blob = TextBlob(headline)
        sentiments.append(blob.sentiment.polarity)
    
    avg_sentiment = np.mean(sentiments)
    
    if avg_sentiment > 0.1:
        label = 'positive'
    elif avg_sentiment < -0.1:
        label = 'negative'
    else:
        label = 'neutral'
    
    return {
        'sentiment_score': float(avg_sentiment),
        'sentiment_label': label,
        'news_count': len(headlines)
    }

def generate_trading_signal(technical: Dict, fundamental: Dict, sentiment: Dict) -> Dict[str, Any]:
    """Genera señal de trading basada en todos los análisis"""
    
    # Scoring técnico
    tech_score = 0.0
    tech_reasons = []
    
    # MA Crossover
    if technical['ma_crossover'] > 0:
        tech_score += 0.3
        tech_reasons.append("MA bullish crossover")
    elif technical['ma_crossover'] < 0:
        tech_score -= 0.3
        tech_reasons.append("MA bearish crossover")
    
    # RSI
    if technical['rsi'] < 30:
        tech_score += 0.2
        tech_reasons.append("RSI oversold")
    elif technical['rsi'] > 70:
        tech_score -= 0.2
        tech_reasons.append("RSI overbought")
    
    # MACD
    if technical['macd_histogram'] > 0:
        tech_score += 0.1
        tech_reasons.append("MACD bullish momentum")
    else:
        tech_score -= 0.1
        tech_reasons.append("MACD bearish momentum")
    
    # Bollinger Bands
    if technical['price_vs_bb_lower'] < 0:
        tech_score += 0.15
        tech_reasons.append("Price below lower Bollinger Band")
    elif technical['price_vs_bb_upper'] < 0:
        tech_score -= 0.15
        tech_reasons.append("Price above upper Bollinger Band")
    
    # Scoring de sentimiento
    sentiment_score = sentiment['sentiment_score'] * 0.3
    
    # Score final
    final_score = tech_score + sentiment_score
    confidence = min(abs(final_score), 1.0)
    
    # Determinar tipo de señal
    if final_score > 0.3:
        signal_type = "buy"
    elif final_score < -0.3:
        signal_type = "sell"
    else:
        signal_type = "hold"
    
    # Calcular tamaño de posición basado en confianza
    position_size = confidence * float(os.getenv('MAX_POSITION_PERCENT', 1.0))
    
    # Generar justificación
    reason_parts = []
    reason_parts.extend(tech_reasons)
    if sentiment['sentiment_label'] != 'neutral':
        reason_parts.append(f"Market sentiment is {sentiment['sentiment_label']}")
    
    reason = ". ".join(reason_parts) + f". Final confidence: {confidence:.2f}"
    
    return {
        'type': signal_type,
        'size': round(position_size, 4),
        'confidence_score': round(confidence, 3),
        'reason': reason,
        'technical_score': round(tech_score, 3),
        'sentiment_score': round(sentiment_score, 3),
        'final_score': round(final_score, 3)
    }

# Endpoints
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "trading-ai-service"}

@app.get("/market-data")
async def get_market_data():
    """Endpoint para obtener datos de mercado (placeholder)"""
    return {
        "data": {
            "ticker": "AAPL",
            "prices": [150.0, 151.2, 149.8, 152.1, 151.0],
            "volumes": [1000000, 1100000, 950000, 1200000, 1050000],
            "timestamps": [
                (datetime.now() - timedelta(minutes=20)).isoformat(),
                (datetime.now() - timedelta(minutes=15)).isoformat(),
                (datetime.now() - timedelta(minutes=10)).isoformat(),
                (datetime.now() - timedelta(minutes=5)).isoformat(),
                datetime.now().isoformat()
            ]
        }
    }

@app.post("/analysis/technical")
async def technical_analysis(request: TechnicalAnalysisRequest):
    """Realiza análisis técnico de los datos de mercado"""
    try:
        market_data = request.market_data
        
        if 'prices' not in market_data or 'volumes' not in market_data:
            raise HTTPException(status_code=400, detail="Missing prices or volumes data")
        
        analysis = calculate_technical_indicators(
            market_data['prices'], 
            market_data['volumes']
        )
        
        return {
            "analysis_type": "technical",
            "timestamp": datetime.now().isoformat(),
            "indicators": analysis
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Technical analysis failed: {str(e)}")

@app.post("/analysis/fundamental")
async def fundamental_analysis(request: FundamentalAnalysisRequest):
    """Realiza análisis fundamental (placeholder)"""
    try:
        return {
            "analysis_type": "fundamental",
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "pe_ratio": 25.4,
                "revenue_growth": 0.12,
                "debt_to_equity": 0.65,
                "fundamental_score": 0.7
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fundamental analysis failed: {str(e)}")

@app.post("/analysis/sentiment")
async def sentiment_analysis(request: SentimentAnalysisRequest):
    """Realiza análisis de sentimiento de noticias"""
    try:
        news_data = request.news_data
        
        if 'headlines' not in news_data:
            raise HTTPException(status_code=400, detail="Missing headlines data")
        
        analysis = analyze_sentiment(news_data['headlines'])
        
        return {
            "analysis_type": "sentiment",
            "timestamp": datetime.now().isoformat(),
            "sentiment": analysis
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sentiment analysis failed: {str(e)}")

@app.post("/signal/generate")
async def generate_signal(request: SignalGenerationRequest):
    """Genera señal de trading basada en todos los análisis"""
    try:
        # Extraer datos de análisis
        technical = request.technical_analysis.get('indicators', {})
        fundamental = request.fundamental_analysis.get('metrics', {})
        sentiment = request.sentiment_analysis.get('sentiment', {})
        
        # Generar señal
        signal = generate_trading_signal(technical, fundamental, sentiment)
        
        return {
            "signal_type": "trading",
            "timestamp": datetime.now().isoformat(),
            "ticker": "AAPL",  # En producción sería dinámico
            **signal
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Signal generation failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
