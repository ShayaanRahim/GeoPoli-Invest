import re
from typing import List, Dict, Any
from scrapers.news_api_client import GEO_KEYWORDS, REGIONS

EVENT_TYPES = {
    "sanctions": ["sanction", "embargo", "ban"],
    "military": ["military", "attack", "strike", "missile", "drone", "war", "conflict"],
    "trade": ["trade", "tariff", "export", "import", "trade war"],
    "energy": ["energy", "oil", "gas", "pipeline", "fuel", "crisis"],
    "diplomacy": ["diplomacy", "negotiation", "talks", "summit"],
    "cyber": ["cyber", "hack", "cyberattack", "ransomware"],
    "political": ["election", "coup", "protest", "vote", "referendum"]
}
SENTIMENT = {
    "negative": ["sanction", "conflict", "attack", "ban", "crisis", "protest", "coup", "war", "embargo"],
    "positive": ["talks", "negotiation", "deal", "agreement", "peace", "summit"],
}

def relevance_score(text: str) -> float:
    """Simple relevance score based on keyword count."""
    text = text.lower()
    return min(1.0, sum(text.count(k) for k in GEO_KEYWORDS) / 5.0)

def extract_countries_regions(text: str) -> (List[str], str):
    """Extracts countries and region from text."""
    found_countries = []
    found_region = None
    for region, names in REGIONS.items():
        for name in names:
            if re.search(rf"\\b{name.lower()}\\b", text.lower()):
                found_countries.append(name)
                found_region = region
    return list(set(found_countries)), found_region

def categorize_event(text: str) -> str:
    """Categorizes event type based on keywords."""
    text = text.lower()
    for event, keywords in EVENT_TYPES.items():
        if any(k in text for k in keywords):
            return event
    return "other"

def sentiment_analysis(text: str) -> str:
    """Basic sentiment analysis for market impact."""
    text = text.lower()
    if any(k in text for k in SENTIMENT["negative"]):
        return "negative"
    if any(k in text for k in SENTIMENT["positive"]):
        return "positive"
    return "neutral"

def process_article(article: Dict[str, Any]) -> Dict[str, Any]:
    """Processes a single news article for all fields."""
    text = (article.get("title", "") + " " + (article.get("content") or "")).strip()
    score = relevance_score(text)
    countries, region = extract_countries_regions(text)
    event_type = categorize_event(text)
    sentiment = sentiment_analysis(text)
    return {
        "id": article.get("raw", {}).get("link", article.get("title", ""))[:64],  # crude unique id
        "title": article.get("title"),
        "content": article.get("content"),
        "source": article.get("source"),
        "publish_date": article.get("publish_date"),
        "relevance_score": score,
        "region": region,
        "countries": countries,
        "event_type": event_type,
        "market_sentiment": sentiment,
        "affected_sectors": [],  # can be filled in later
    } 