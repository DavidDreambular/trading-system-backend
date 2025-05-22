-- Trading System Database Schema
-- Crear extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabla de señales de trading
CREATE TABLE IF NOT EXISTS trading_signals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticker VARCHAR(10) NOT NULL,
    signal_type VARCHAR(10) NOT NULL CHECK (signal_type IN ('buy', 'sell', 'hold')),
    size DECIMAL(10, 4) NOT NULL,
    confidence_score DECIMAL(5, 3) NOT NULL CHECK (confidence_score >= 0 AND confidence_score <= 1),
    reason TEXT NOT NULL,
    technical_score DECIMAL(5, 3),
    sentiment_score DECIMAL(5, 3),
    final_score DECIMAL(5, 3),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected', 'executed', 'cancelled')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    approved_at TIMESTAMP WITH TIME ZONE,
    executed_at TIMESTAMP WITH TIME ZONE,
    execution_price DECIMAL(10, 4),
    execution_id VARCHAR(100),
    approved_by VARCHAR(100),
    notes TEXT
);

-- Tabla de datos de mercado históricos
CREATE TABLE IF NOT EXISTS market_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticker VARCHAR(10) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    open_price DECIMAL(10, 4) NOT NULL,
    high_price DECIMAL(10, 4) NOT NULL,
    low_price DECIMAL(10, 4) NOT NULL,
    close_price DECIMAL(10, 4) NOT NULL,
    volume BIGINT NOT NULL,
    source VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para optimización
CREATE INDEX IF NOT EXISTS idx_trading_signals_ticker ON trading_signals(ticker);
CREATE INDEX IF NOT EXISTS idx_trading_signals_status ON trading_signals(status);
CREATE INDEX IF NOT EXISTS idx_trading_signals_created_at ON trading_signals(created_at);
CREATE INDEX IF NOT EXISTS idx_market_data_ticker_timestamp ON market_data(ticker, timestamp);

-- Función para actualizar estado de señales
CREATE OR REPLACE FUNCTION update_signal_status(
    signal_uuid UUID,
    new_status VARCHAR(20),
    approved_by_user VARCHAR(100) DEFAULT NULL
) RETURNS BOOLEAN AS $$
BEGIN
    UPDATE trading_signals 
    SET 
        status = new_status,
        approved_at = CASE WHEN new_status = 'approved' THEN NOW() ELSE approved_at END,
        approved_by = CASE WHEN new_status = 'approved' THEN approved_by_user ELSE approved_by END,
        executed_at = CASE WHEN new_status = 'executed' THEN NOW() ELSE executed_at END
    WHERE id = signal_uuid;
    
    RETURN FOUND;
END;
$$ LANGUAGE plpgsql;
