#!/usr/bin/env python3
"""
Geopolitical News Analysis Flask Application
A professional Flask server for analyzing geopolitical news and their market impact.
"""

import os
import logging
import time
from datetime import datetime, timedelta
from functools import wraps
from typing import Dict, List, Optional, Any

from flask import Flask, jsonify, request, abort, make_response, send_from_directory
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
import requests

# Import our configuration
from config import get_config, validate_required_keys, is_geopolitical_event, get_affected_sectors, get_sector_stocks
from scrapers.news_api_client import fetch_news_from_newsdata, filter_geopolitical_news
from analyzers.news_processor import process_article
from database import init_db, store_news_articles, get_latest_news, get_news_by_region

# Initialize Flask app
app = Flask(__name__)

# Load configuration
config = get_config()
app.config.from_object(config)
init_db()  # Ensure DB tables are created before serving requests

# Enable CORS for all origins (for local dev)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Rate limiting storage (in production, use Redis)
request_counts = {}

def rate_limit(f):
    """Rate limiting decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not config.RATE_LIMIT_ENABLED:
            return f(*args, **kwargs)
        
        client_ip = request.remote_addr
        current_time = time.time()
        
        # Clean old entries
        request_counts.clear()
        
        # Check rate limit
        if client_ip in request_counts:
            count, timestamp = request_counts[client_ip]
            if current_time - timestamp < config.RATE_LIMIT_WINDOW:
                if count >= config.RATE_LIMIT_REQUESTS:
                    return jsonify({
                        'error': 'Rate limit exceeded',
                        'message': f'Maximum {config.RATE_LIMIT_REQUESTS} requests per {config.RATE_LIMIT_WINDOW} seconds'
                    }), 429
                request_counts[client_ip] = (count + 1, timestamp)
            else:
                request_counts[client_ip] = (1, current_time)
        else:
            request_counts[client_ip] = (1, current_time)
        
        return f(*args, **kwargs)
    return decorated_function

def validate_api_key(api_key: str, service: str) -> bool:
    """Validate API key format"""
    if not api_key:
        logger.warning(f"Missing {service} API key")
        return False
    return True

def analyze_geopolitical_impact(news_text: str) -> Dict[str, Any]:
    """Analyze the geopolitical impact of news (placeholder for LLM integration)"""
    try:
        # Check if it's a geopolitical event
        is_geopolitical = is_geopolitical_event(news_text)
        
        if not is_geopolitical:
            return {
                'is_geopolitical': False,
                'impact_level': 'none',
                'affected_sectors': [],
                'confidence': 0.0
            }
        
        # Get affected sectors
        affected_sectors = get_affected_sectors(news_text)
        
        # Simple impact analysis (replace with LLM in production)
        impact_keywords = ['war', 'sanctions', 'embargo', 'crisis', 'attack']
        impact_level = 'low'
        if any(keyword in news_text.lower() for keyword in impact_keywords):
            impact_level = 'high'
        elif any(keyword in news_text.lower() for keyword in ['tension', 'dispute', 'protest']):
            impact_level = 'medium'
        
        return {
            'is_geopolitical': True,
            'impact_level': impact_level,
            'affected_sectors': affected_sectors,
            'confidence': 0.8 if impact_level == 'high' else 0.6,
            'analysis': f"This appears to be a {impact_level} impact geopolitical event affecting {', '.join(affected_sectors) if affected_sectors else 'various'} sectors."
        }
        
    except Exception as e:
        logger.error(f"Error analyzing geopolitical impact: {e}")
        return {
            'is_geopolitical': False,
            'impact_level': 'unknown',
            'affected_sectors': [],
            'confidence': 0.0,
            'error': str(e)
        }

def get_stock_data(symbols: List[str]) -> Dict[str, Any]:
    """Get stock data from Alpha Vantage (placeholder)"""
    if not validate_api_key(config.ALPHA_VANTAGE_STOCK_API_KEY, "Alpha Vantage"):
        return {}
    
    try:
        # This is a placeholder - implement actual Alpha Vantage API calls
        stock_data = {}
        for symbol in symbols[:5]:  # Limit to 5 symbols for demo
            stock_data[symbol] = {
                'price': 100.0,  # Placeholder
                'change': 1.5,
                'change_percent': 1.5,
                'volume': 1000000,
                'market_cap': 1000000000
            }
        
        return stock_data
        
    except Exception as e:
        logger.error(f"Error fetching stock data: {e}")
        return {}

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP Exception: {e.code} - {e.description}")
    return jsonify({
        'error': e.description,
        'code': e.code
    }), e.code

@app.errorhandler(Exception)
def handle_generic_exception(e):
    """Handle generic exceptions"""
    logger.error(f"Unexpected error: {e}")
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

@app.route('/api/health')
@rate_limit
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0',
        'services': {
            'news_api': bool(config.NEWSDATA_API_KEY),
            'stock_api': bool(config.ALPHA_VANTAGE_STOCK_API_KEY),
            'llm_api': bool(config.OPENAI_API_KEY)
        }
    })

@app.route('/api/news')
@rate_limit
def get_news():
    """Get real-time geopolitical news"""
    try:
        # Get query parameters
        limit = request.args.get('limit', config.MAX_NEWS_ARTICLES, type=int)
        category = request.args.get('category', 'geopolitical')
        
        # Fetch news
        articles = fetch_news_from_newsdata(limit)
        
        # Filter and limit results
        if articles:
            # Filter for geopolitical relevance
            geopolitical_articles = filter_geopolitical_news(articles)
            
            articles = geopolitical_articles[:limit]
        
        return jsonify({
            'status': 'success',
            'count': len(articles),
            'articles': articles,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in get_news: {e}")
        return jsonify({
            'error': 'Failed to fetch news',
            'message': str(e)
        }), 500

@app.route('/api/impact', methods=['POST'])
@rate_limit
def analyze_impact():
    """Analyze the impact of geopolitical events"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Missing required field: text'
            }), 400
        
        news_text = data['text']
        
        # Analyze impact
        impact_analysis = analyze_geopolitical_impact(news_text)
        
        # Get affected stocks if sectors are identified
        affected_stocks = {}
        if impact_analysis.get('affected_sectors'):
            for sector in impact_analysis['affected_sectors']:
                stocks = get_sector_stocks(sector)
                if stocks:
                    affected_stocks[sector] = stocks
        
        return jsonify({
            'status': 'success',
            'analysis': impact_analysis,
            'affected_stocks': affected_stocks,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in analyze_impact: {e}")
        return jsonify({
            'error': 'Failed to analyze impact',
            'message': str(e)
        }), 500

@app.route('/api/historical')
@rate_limit
def get_historical():
    """Get historical data on similar events"""
    try:
        # Get query parameters
        event_type = request.args.get('event_type', 'general')
        days_back = request.args.get('days', 30, type=int)
        
        # Placeholder historical data
        historical_data = {
            'event_type': event_type,
            'period_days': days_back,
            'similar_events': [
                {
                    'date': '2023-01-15',
                    'event': 'Trade sanctions imposed',
                    'market_impact': -2.5,
                    'affected_sectors': ['trade', 'shipping'],
                    'recovery_time_days': 7
                },
                {
                    'date': '2022-11-20',
                    'event': 'Political crisis',
                    'market_impact': -1.8,
                    'affected_sectors': ['finance', 'consumer'],
                    'recovery_time_days': 5
                }
            ],
            'average_impact': -2.15,
            'average_recovery_time': 6
        }
        
        return jsonify({
            'status': 'success',
            'data': historical_data,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in get_historical: {e}")
        return jsonify({
            'error': 'Failed to fetch historical data',
            'message': str(e)
        }), 500

@app.route('/api/stocks/<sector>')
@rate_limit
def get_sector_stocks_api(sector):
    """Get stocks for a specific sector"""
    try:
        stocks = get_sector_stocks(sector)
        
        if not stocks:
            return jsonify({
                'error': f'No stocks found for sector: {sector}'
            }), 404
        
        # Get stock data
        stock_data = get_stock_data(stocks)
        
        return jsonify({
            'status': 'success',
            'sector': sector,
            'stocks': stocks,
            'stock_data': stock_data,
            'count': len(stocks),
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in get_sector_stocks_api: {e}")
        return jsonify({
            'error': 'Failed to fetch sector stocks',
            'message': str(e)
        }), 500

@app.route('/api/analysis/full', methods=['POST'])
@rate_limit
def full_analysis():
    """Perform full analysis: news + impact + historical + stocks"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Missing required field: text'
            }), 400
        
        news_text = data['text']
        
        # Step 1: Analyze impact
        impact_analysis = analyze_geopolitical_impact(news_text)
        
        # Step 2: Get affected sectors and stocks
        affected_sectors = impact_analysis.get('affected_sectors', [])
        affected_stocks = {}
        stock_data = {}
        
        if affected_sectors:
            for sector in affected_sectors:
                stocks = get_sector_stocks(sector)
                if stocks:
                    affected_stocks[sector] = stocks
                    sector_data = get_stock_data(stocks)
                    stock_data.update(sector_data)
        
        # Step 3: Get historical context
        event_type = 'general'
        if any(keyword in news_text.lower() for keyword in ['sanctions', 'embargo']):
            event_type = 'sanctions'
        elif any(keyword in news_text.lower() for keyword in ['war', 'conflict']):
            event_type = 'conflict'
        
        historical_data = {
            'event_type': event_type,
            'similar_events': [
                {
                    'date': '2023-01-15',
                    'event': 'Similar event',
                    'market_impact': -2.5,
                    'recovery_time_days': 7
                }
            ]
        }
        
        return jsonify({
            'status': 'success',
            'analysis': {
                'impact': impact_analysis,
                'affected_sectors': affected_sectors,
                'affected_stocks': affected_stocks,
                'stock_data': stock_data,
                'historical_context': historical_data
            },
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in full_analysis: {e}")
        return jsonify({
            'error': 'Failed to perform full analysis',
            'message': str(e)
        }), 500

@app.route('/api/config/validate')
@rate_limit
def validate_config():
    """Validate API configuration"""
    try:
        validation_result = validate_required_keys()
        
        return jsonify({
            'status': 'success' if validation_result else 'warning',
            'validation': {
                'news_api': bool(config.NEWSDATA_API_KEY),
                'stock_api': bool(config.ALPHA_VANTAGE_STOCK_API_KEY),
                'llm_api': bool(config.OPENAI_API_KEY),
                'all_required': validation_result
            },
            'missing_keys': [] if validation_result else ['Some optional API keys missing'],
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in validate_config: {e}")
        return jsonify({
            'error': 'Failed to validate configuration',
            'message': str(e)
        }), 500

@app.route('/api/news/refresh', methods=['POST'])
def refresh_news():
    """Trigger news collection and processing."""
    raw_articles = fetch_news_from_newsdata(limit=20)
    filtered = filter_geopolitical_news(raw_articles)
    processed = [process_article(a) for a in filtered]
    store_news_articles(processed)
    return jsonify({"status": "success", "fetched": len(processed)})

@app.route('/api/news/latest')
def latest_news():
    """Get latest processed news."""
    news = get_latest_news(limit=20)
    return jsonify({"news": news})

@app.route('/api/news/by-region/<region>')
def news_by_region(region):
    """Get news filtered by region."""
    news = get_news_by_region(region, limit=20)
    return jsonify({"news": news})

# Serve static files from the frontend directory
@app.route('/')
@app.route('/<path:path>')
def serve_frontend(path='index.html'):
    frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend'))
    if path != "" and os.path.exists(os.path.join(frontend_dir, path)):
        return send_from_directory(frontend_dir, path)
    else:
        return send_from_directory(frontend_dir, 'index.html')

if __name__ == '__main__':
    # Validate configuration on startup
    logger.info("Starting Geopolitical News Analysis Server...")
    validate_required_keys()
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5001)),
        debug=config.DEBUG
    )