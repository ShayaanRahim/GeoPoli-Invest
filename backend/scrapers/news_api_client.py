import logging
import requests
from typing import List, Dict, Any

NEWSAPI_KEY = "ca7a28ec5ae54e6194fc639fd6764ae9"
NEWSAPI_URL = "https://newsapi.org/v2/everything"

GEO_KEYWORDS = [
    "geopolitics", "conflict", "sanctions", "military", "diplomacy", "energy crisis",
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
logger = logging.getLogger(__name__)

def fetch_news_from_newsapi(limit=20) -> List[Dict[str, Any]]:
    """Fetches news from NewsAPI.org and returns a list of articles."""
    params = {
        "q": " OR ".join(GEO_KEYWORDS),
        "language": "en",
        "pageSize": min(limit, 20),
        "apiKey": NEWSAPI_KEY,
        "sortBy": "publishedAt"
    }
    try:
        resp = requests.get(NEWSAPI_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") != "ok":
            logger.error(f"NewsAPI.org error: {data.get('message')}")
            logger.error(f"Full response: {data}")
            return []
        articles = data.get("articles", [])
        return [
            {
                "title": a.get("title"),
                "content": a.get("content") or a.get("description"),
                "source": a.get("source", {}).get("name"),
                "publish_date": a.get("publishedAt"),
                "url": a.get("url"),
                "raw": a
            }
            for a in articles
        ]
    except Exception as e:
        logger.error(f"Failed to fetch news: {e}")
        return []

def fetch_news_from_newsdata(limit=20) -> List[Dict[str, Any]]:
    # For compatibility with the rest of the backend
    return fetch_news_from_newsapi(limit)

def filter_geopolitical_news(articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filters articles for geopolitical relevance based on keywords."""
    filtered = []
    for article in articles:
        text = (article.get("title", "") + " " + (article.get("content") or "")).lower()
        if any(k in text for k in GEO_KEYWORDS):
            filtered.append(article)
    return filtered 