// SMTP Email Service - Reemplaza Slack notifications
// Agregar al data-service para envío de emails

const nodemailer = require('nodemailer');

// Configuración SMTP
const smtpConfig = {
  host: process.env.SMTP_HOST || 'smtp.hostinger.com',
  port: parseInt(process.env.SMTP_PORT) || 587,
  secure: false, // true for 465, false for other ports
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS
  }
};

// Crear transporter
let transporter;
if (process.env.SMTP_USER && process.env.SMTP_PASS) {
  transporter = nodemailer.createTransporter(smtpConfig);
  console.log('SMTP transporter configured');
} else {
  console.log('SMTP not configured - using console logs');
}

// Función para enviar emails de trading signals
async function sendTradingSignalEmail(signalData) {
  if (!transporter) {
    console.log('SMTP not configured, would send email:', signalData);
    return false;
  }

  try {
    const emailHTML = `
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
            .container { background: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: 0 auto; }
            .header { background: #2c3e50; color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; margin: -30px -30px 20px -30px; }
            .signal-type { font-size: 24px; font-weight: bold; text-transform: uppercase; }
            .signal-buy { color: #27ae60; }
            .signal-sell { color: #e74c3c; }
            .signal-hold { color: #f39c12; }
            .details { background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 15px 0; }
            .confidence { font-size: 18px; font-weight: bold; }
            .reason { font-style: italic; margin: 10px 0; }
            .footer { text-align: center; color: #7f8c8d; font-size: 12px; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎯 Trading Signal Alert</h1>
                <div class="signal-type signal-${signalData.type}">${signalData.type.toUpperCase()}</div>
            </div>
            
            <div class="details">
                <p><strong>Symbol:</strong> ${signalData.ticker || 'Unknown'}</p>
                <p><strong>Size:</strong> ${signalData.size || 'N/A'}</p>
                <p class="confidence"><strong>Confidence:</strong> ${Math.round((signalData.confidence_score || 0) * 100)}%</p>
                <p class="reason"><strong>Reason:</strong> ${signalData.reason || 'No reason provided'}</p>
            </div>
            
            <div class="details">
                <p><strong>Technical Score:</strong> ${signalData.technical_score || 'N/A'}</p>
                <p><strong>Sentiment Score:</strong> ${signalData.sentiment_score || 'N/A'}</p>
                <p><strong>Final Score:</strong> ${signalData.final_score || 'N/A'}</p>
            </div>
            
            <div class="footer">
                <p>Generated at: ${new Date().toLocaleString()}</p>
                <p>Trading System - Safe Tag Agency</p>
            </div>
        </div>
    </body>
    </html>
    `;

    const mailOptions = {
      from: `"Trading System" <${process.env.SMTP_USER}>`,
      to: process.env.NOTIFICATION_EMAIL || process.env.SMTP_USER,
      subject: `🎯 Trading Signal: ${signalData.type?.toUpperCase()} ${signalData.ticker || 'Signal'}`,
      html: emailHTML
    };

    const info = await transporter.sendMail(mailOptions);
    console.log('Trading signal email sent:', info.messageId);
    return true;

  } catch (error) {
    console.error('Error sending email:', error);
    return false;
  }
}

// Endpoint para enviar notificaciones por email
app.post('/notify/email', async (req, res) => {
  try {
    const signalData = req.body;
    
    const success = await sendTradingSignalEmail(signalData);
    
    res.json({
      success: success,
      message: success ? 'Email sent successfully' : 'Failed to send email',
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    console.error('Email notification error:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Función de test para SMTP
app.get('/test/email', async (req, res) => {
  try {
    const testSignal = {
      type: 'buy',
      ticker: 'AAPL',
      size: 0.5,
      confidence_score: 0.85,
      reason: 'Strong technical indicators with positive sentiment',
      technical_score: 0.7,
      sentiment_score: 0.6,
      final_score: 0.85
    };

    const success = await sendTradingSignalEmail(testSignal);
    
    res.json({
      success: success,
      message: 'Test email sent',
      smtp_configured: !!transporter,
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message,
      smtp_configured: !!transporter,
      timestamp: new Date().toISOString()
    });
  }
});
