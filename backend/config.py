import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Database Configuration
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///geopoli_news.db'
    
    # News API Configuration
    # Multiple news API options for redundancy
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
    NEWS_API_BASE_URL = 'https://newsdata.io/api/1/news'
    
    # NewsData.io specific configuration
    NEWSDATA_API_KEY = os.environ.get('NEWS_API_KEY')  # Using same env var
    NEWSDATA_BASE_URL = 'https://newsdata.io/api/1/news'
    
    # Alternative news APIs
    ALPHA_VANTAGE_API_KEY = os.environ.get('ALPHA_VANTAGE_API_KEY')
    ALPHA_VANTAGE_BASE_URL = 'https://www.alphavantage.co/query'
    
    # Reuters API (if available)
    REUTERS_API_KEY = os.environ.get('REUTERS_API_KEY')
    REUTERS_BASE_URL = 'https://api.reuters.com'
    
    # LLM Configuration
    # OpenAI Configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-4')
    OPENAI_MAX_TOKENS = int(os.environ.get('OPENAI_MAX_TOKENS', '2000'))
    OPENAI_TEMPERATURE = float(os.environ.get('OPENAI_TEMPERATURE', '0.3'))
    
    # Alternative LLM options
    ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
    ANTHROPIC_MODEL = os.environ.get('ANTHROPIC_MODEL', 'claude-3-sonnet-20240229')
    
    # Cohere API (alternative)
    COHERE_API_KEY = os.environ.get('COHERE_API_KEY')
    COHERE_MODEL = os.environ.get('COHERE_MODEL', 'command')
    
    # Stock Market Data APIs
    # Alpha Vantage for stock data
    ALPHA_VANTAGE_STOCK_API_KEY = (
        os.environ.get('ALPHA_VANTAGE_STOCK_API_KEY') or 
        os.environ.get('ALPHA_VANTAGE_API_KEY')
    )
    
    # Yahoo Finance (free alternative)
    YAHOO_FINANCE_ENABLED = os.environ.get('YAHOO_FINANCE_ENABLED', 'True').lower() == 'true'
    
    # IEX Cloud (alternative)
    IEX_API_KEY = os.environ.get('IEX_API_KEY')
    IEX_BASE_URL = 'https://cloud.iexapis.com/stable'
    
    # Stock Sectors for Analysis
    SECTORS = {
        'energy': ['XOM', 'CVX', 'COP', 'EOG', 'SLB', 'HAL', 'KMI', 'PSX'],
        'defense': ['LMT', 'RTX', 'NOC', 'GD', 'BA', 'LHX', 'TDG', 'AJRD'],
        'airlines': ['DAL', 'UAL', 'AAL', 'LUV', 'JBLU', 'ALK', 'SAVE', 'SKYW'],
        'shipping': ['FDX', 'UPS', 'CHRW', 'EXPD', 'XPO', 'ODFL', 'JBHT', 'LSTR'],
        'tech': ['AAPL', 'MSFT', 'GOOGL', 'META', 'NVDA', 'TSLA', 'AMZN', 'NFLX'],
        'finance': ['JPM', 'BAC', 'WFC', 'GS', 'MS', 'C', 'USB', 'PNC'],
        'healthcare': ['JNJ', 'PFE', 'UNH', 'ABBV', 'MRK', 'TMO', 'ABT', 'DHR'],
        'consumer': ['PG', 'KO', 'PEP', 'WMT', 'HD', 'MCD', 'SBUX', 'NKE'],
        'materials': ['LIN', 'APD', 'FCX', 'NEM', 'DOW', 'DD', 'CAT', 'DE']
    }
    
    # Geopolitical Keywords for Event Detection
    GEOPOLITICAL_KEYWORDS = [
        # Conflicts and Wars
        'war', 'conflict', 'military', 'invasion', 'attack', 'battle', 'combat',
        'ceasefire', 'peace talks', 'diplomatic', 'treaty', 'alliance',
        
        # Economic Sanctions and Trade
        'sanctions', 'embargo', 'trade war', 'tariffs', 'trade dispute',
        'economic sanctions', 'financial sanctions', 'export ban', 'import ban',
        
        # Political Events
        'election', 'coup', 'protest', 'revolution', 'regime change',
        'political crisis', 'government shutdown', 'impeachment', 'referendum',
        
        # Natural Disasters and Crises
        'natural disaster', 'earthquake', 'tsunami', 'hurricane', 'flood',
        'drought', 'famine', 'pandemic', 'outbreak', 'crisis',
        
        # Energy and Resources
        'oil embargo', 'energy crisis', 'gas shortage', 'fuel prices',
        'renewable energy', 'climate change', 'carbon tax', 'green energy',
        
        # Infrastructure and Technology
        'cyber attack', 'hacking', 'data breach', 'infrastructure',
        'power grid', 'internet shutdown', 'digital currency', 'blockchain',
        
        # Regional Keywords
        'middle east', 'eastern europe', 'south china sea', 'baltic sea',
        'strait of hormuz', 'suez canal', 'panama canal', 'arctic',
        
        # International Relations
        'nato', 'united nations', 'g7', 'g20', 'brics', 'eu', 'brexit',
        'international court', 'icc', 'world bank', 'imf'
    ]
    
    # Redis Configuration (for caching and background tasks)
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', REDIS_URL)
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', REDIS_URL)
    
    # Application Settings
    MAX_NEWS_ARTICLES = int(os.environ.get('MAX_NEWS_ARTICLES', '50'))
    NEWS_UPDATE_INTERVAL = int(os.environ.get('NEWS_UPDATE_INTERVAL', '300'))  # 5 minutes in seconds
    
    # Impact Analysis Settings
    IMPACT_ANALYSIS_ENABLED = os.environ.get('IMPACT_ANALYSIS_ENABLED', 'True').lower() == 'true'
    HISTORICAL_ANALYSIS_ENABLED = os.environ.get('HISTORICAL_ANALYSIS_ENABLED', 'True').lower() == 'true'
    
    # Caching Configuration
    CACHE_ENABLED = os.environ.get('CACHE_ENABLED', 'True').lower() == 'true'
    CACHE_TIMEOUT = int(os.environ.get('CACHE_TIMEOUT', '3600'))  # 1 hour in seconds
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'geopoli_news.log')
    
    # Rate Limiting
    RATE_LIMIT_ENABLED = os.environ.get('RATE_LIMIT_ENABLED', 'True').lower() == 'true'
    RATE_LIMIT_REQUESTS = int(os.environ.get('RATE_LIMIT_REQUESTS', '100'))
    RATE_LIMIT_WINDOW = int(os.environ.get('RATE_LIMIT_WINDOW', '3600'))  # 1 hour
    
    # Security Settings
    CORS_ENABLED = os.environ.get('CORS_ENABLED', 'True').lower() == 'true'
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Error Handling
    SEND_ERROR_REPORTS = os.environ.get('SEND_ERROR_REPORTS', 'False').lower() == 'true'
    
    @staticmethod
    def init_app(app):
        """Initialize application with configuration"""
        pass

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Production-specific configurations
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not app.debug and not app.testing:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler(
                'logs/geopoli_news.log', 
                maxBytes=10240000, 
                backupCount=10
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            app.logger.setLevel(logging.INFO)
            app.logger.info('Geopoli News startup')

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# Helper functions for configuration
def get_config():
    """Get configuration based on environment"""
    config_name = os.environ.get('FLASK_CONFIG') or 'default'
    return config[config_name]

def validate_required_keys():
    """Validate that required API keys are present"""
    required_keys = {
        'NEWS_API_KEY': 'News API key for fetching geopolitical news',
        'OPENAI_API_KEY': 'OpenAI API key for impact analysis',
        'ALPHA_VANTAGE_API_KEY': 'Alpha Vantage API key for stock data'
    }
    
    missing_keys = []
    for key, description in required_keys.items():
        if not os.environ.get(key):
            missing_keys.append(f"{key}: {description}")
    
    if missing_keys:
        print("Warning: Missing required API keys:")
        for key in missing_keys:
            print(f"  - {key}")
        print("\nPlease set these environment variables or add them to a .env file")
        return False
    
    return True

def get_sector_stocks(sector_name):
    """Get list of stocks for a given sector"""
    return Config.SECTORS.get(sector_name.lower(), [])

def get_all_stocks():
    """Get all stocks across all sectors"""
    all_stocks = []
    for stocks in Config.SECTORS.values():
        all_stocks.extend(stocks)
    return list(set(all_stocks))  # Remove duplicates

def is_geopolitical_event(text):
    """Check if text contains geopolitical keywords"""
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in Config.GEOPOLITICAL_KEYWORDS)

def get_affected_sectors(event_text):
    """Determine which sectors might be affected by a geopolitical event"""
    text_lower = event_text.lower()
    affected_sectors = []
    
    # Simple keyword-based sector mapping
    sector_keywords = {
        'energy': ['oil', 'gas', 'energy', 'petroleum', 'renewable', 'solar', 'wind'],
        'defense': ['military', 'defense', 'weapons', 'nato', 'army', 'navy', 'air force'],
        'airlines': ['airline', 'aviation', 'flight', 'airport', 'travel'],
        'shipping': ['shipping', 'cargo', 'freight', 'logistics', 'supply chain'],
        'tech': ['technology', 'cyber', 'digital', 'internet', 'software'],
        'finance': ['bank', 'financial', 'currency', 'market', 'trading'],
        'healthcare': ['health', 'medical', 'pharmaceutical', 'hospital'],
        'consumer': ['retail', 'consumer', 'shopping', 'goods'],
        'materials': ['steel', 'aluminum', 'copper', 'mining', 'chemicals']
    }
    
    for sector, keywords in sector_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            affected_sectors.append(sector)
    
    return affected_sectors

# Validate configuration on import
if __name__ == '__main__':
    validate_required_keys()
