import logging
import requests
from typing import List, Dict, Any
from config import get_config

config = get_config()
logger = logging.getLogger(__name__)

GEO_KEYWORDS = [
    "sanctions", "conflict", "trade war", "military", "diplomacy", "energy crisis",
    "embargo", "protest", "election", "coup", "nuclear", "missile", "cyberattack"
]
REGIONS = {
    "US": ["United States", "America", "US", "USA"],
    "China": ["China", "PRC"],
    "Russia": ["Russia", "Russian"],
    "Iran": ["Iran", "Tehran"],
    "Middle East": ["Middle East", "Saudi", "UAE", "Qatar", "Iraq", "Syria", "Israel", "Palestine"],
    "Europe": ["Europe", "EU", "Germany", "France", "UK", "Britain", "Italy", "Spain"]
}

def fetch_news_from_newsdata(limit=20) -> List[Dict[str, Any]]:
    """Fetches news from NewsData.io API and returns a list of articles."""
    url = config.NEWSDATA_BASE_URL
    params = {
        "apikey": config.NEWSDATA_API_KEY,
        "q": " OR ".join(GEO_KEYWORDS),
        "language": "en",
        "size": min(limit, 20)
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") != "success":
            logger.error(f"NewsData.io API error: {data.get('message')}")
            return []
        articles = data.get("results", [])
        return [
            {
                "title": a.get("title"),
                "content": a.get("content") or a.get("description"),
                "source": a.get("source_id"),
                "publish_date": a.get("pubDate"),
                "raw": a
            }
            for a in articles
        ]
    except Exception as e:
        logger.error(f"Failed to fetch news: {e}")
        return []

def filter_geopolitical_news(articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filters articles for geopolitical relevance based on keywords."""
    filtered = []
    for article in articles:
        text = (article.get("title", "") + " " + (article.get("content") or "")).lower()
        if any(k in text for k in GEO_KEYWORDS):
            filtered.append(article)
    return filtered 