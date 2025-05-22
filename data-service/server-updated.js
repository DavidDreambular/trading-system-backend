/**
 * Data Service - Servicio de Ingesta de Datos de Mercado
 * Con APIs reales y notificaciones SMTP
 */

const express = require('express');
const axios = require('axios');
const Redis = require('redis');
const cors = require('cors');
const rateLimit = require('express-rate-limit');
const nodemailer = require('nodemailer');

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

// SMTP Configuration
const smtpConfig = {
  host: process.env.SMTP_HOST || 'smtp.hostinger.com',
  port: parseInt(process.env.SMTP_PORT) || 587,
  secure: false,
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS
  }
};

let transporter;
if (process.env.SMTP_USER && process.env.SMTP_PASS) {
  transporter = nodemailer.createTransporter(smtpConfig);
  console.log('✅ SMTP configured for notifications');
} else {
  console.log('⚠️ SMTP not configured');
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

console.log('🔑 API Configuration:');
console.log('Alpha Vantage:', config.alphaVantage.apiKey ? '✅ Configured' : '❌ Missing');
console.log('NewsAPI:', config.newsApi.apiKey ? '✅ Configured' : '❌ Missing');
console.log('IEX Cloud:', config.iex.apiKey ? '✅ Configured' : '❌ Missing');
