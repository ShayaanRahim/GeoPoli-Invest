# Geopolitical News Application

A web application that analyzes real-time geopolitical news and assesses their impact on stocks and industries using AI-powered analysis.

## Features

- **Real-time News Fetching**: Get the latest geopolitical news from multiple sources
- **AI Impact Analysis**: Use LLMs to assess the potential impact of geopolitical events
- **Historical Analysis**: Compare current events with similar historical events
- **Stock Market Correlation**: Identify affected stocks and industries
- **RESTful API**: Clean API endpoints for frontend integration

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the root directory with the following variables:

```bash
# Flask Configuration
SECRET_KEY=your-secret-key-change-in-production
FLASK_DEBUG=True
FLASK_CONFIG=development

# Database Configuration
DATABASE_URL=sqlite:///geopoli_news.db

# News API Configuration
NEWS_API_KEY=your-news-api-key-here
ALPHA_VANTAGE_API_KEY=your-alpha-vantage-api-key-here
REUTERS_API_KEY=your-reuters-api-key-here

# LLM Configuration
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=2000
OPENAI_TEMPERATURE=0.3

# Alternative LLM APIs
ANTHROPIC_API_KEY=your-anthropic-api-key-here
ANTHROPIC_MODEL=claude-3-sonnet-20240229
COHERE_API_KEY=your-cohere-api-key-here
COHERE_MODEL=command

# Stock Market Data APIs
ALPHA_VANTAGE_STOCK_API_KEY=your-alpha-vantage-stock-api-key-here
YAHOO_FINANCE_ENABLED=True
IEX_API_KEY=your-iex-api-key-here

# Application Settings
MAX_NEWS_ARTICLES=50
NEWS_UPDATE_INTERVAL=300
IMPACT_ANALYSIS_ENABLED=True
HISTORICAL_ANALYSIS_ENABLED=True

# Caching and Performance
CACHE_ENABLED=True
CACHE_TIMEOUT=3600

# Logging
LOG_LEVEL=INFO
LOG_FILE=geopoli_news.log

# Rate Limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600

# Security
CORS_ENABLED=True
CORS_ORIGINS=*

# Error Handling
SEND_ERROR_REPORTS=False
```

### 3. Required API Keys

You'll need to obtain API keys from the following services:

#### News APIs
- **NewsAPI.org**: [Get API Key](https://newsapi.org/register)
- **Alpha Vantage**: [Get API Key](https://www.alphavantage.co/support/#api-key)
- **Reuters API**: [Get API Key](https://developers.reuters.com/)

#### LLM Services
- **OpenAI**: [Get API Key](https://platform.openai.com/api-keys)
- **Anthropic**: [Get API Key](https://console.anthropic.com/)
- **Cohere**: [Get API Key](https://cohere.ai/)

#### Stock Market Data
- **Alpha Vantage**: [Get API Key](https://www.alphavantage.co/support/#api-key)
- **IEX Cloud**: [Get API Key](https://iexcloud.io/cloud-login#/register)

### 4. Run the Application

```bash
cd backend
python mainApp.py
```

The application will be available at `http://localhost:5000`

## API Endpoints

- `GET /api/news` - Get real-time geopolitical news
- `GET /api/impact` - Analyze impact of geopolitical events
- `GET /api/historical` - Get historical data on similar events

## Project Structure

```
GeoPoli News/
├── backend/
│   ├── config.py          # Configuration management
│   ├── database.py        # Database models and operations
│   ├── mainApp.py         # Main Flask application
│   └── models.py          # Data models
├── frontend/
│   └── index.html         # Frontend interface
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Configuration

The application uses a flexible configuration system with three environments:

- **Development**: Debug mode enabled, detailed logging
- **Production**: Optimized for production deployment
- **Testing**: In-memory database, testing-specific settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
