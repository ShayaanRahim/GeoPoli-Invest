import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, NewsArticle
from config import get_config
from datetime import datetime

config = get_config()
DATABASE_URL = config.DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def store_news_articles(articles):
    session = SessionLocal()
    for a in articles:
        if not session.query(NewsArticle).filter_by(id=a["id"]).first():
            news = NewsArticle(
                id=a["id"],
                title=a["title"],
                content=a["content"],
                source=a["source"],
                publish_date=parse_datetime(a["publish_date"]),
                relevance_score=a["relevance_score"],
                region=a["region"],
                countries=",".join(a["countries"]) if a["countries"] else "",
                event_type=a["event_type"],
                market_sentiment=a["market_sentiment"],
                affected_sectors=",".join(a.get("affected_sectors", [])) if a.get("affected_sectors") else ""
            )
            session.add(news)
    session.commit()
    session.close()

def get_latest_news(limit=20):
    session = SessionLocal()
    news = session.query(NewsArticle).order_by(NewsArticle.publish_date.desc()).limit(limit).all()
    session.close()
    return [serialize_news(n) for n in news]

def get_news_by_region(region, limit=20):
    session = SessionLocal()
    news = session.query(NewsArticle).filter_by(region=region).order_by(NewsArticle.publish_date.desc()).limit(limit).all()
    session.close()
    return [serialize_news(n) for n in news]

def parse_datetime(dt_str):
    if not dt_str:
        return None
    try:
        # Try ISO format first
        return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
    except Exception:
        try:
            # Try common news API format
            return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S%z")
        except Exception:
            return None

def serialize_news(news):
    return {
        "id": news.id,
        "title": news.title,
        "content": news.content,
        "source": news.source,
        "publish_date": news.publish_date.isoformat() if news.publish_date else None,
        "relevance_score": news.relevance_score,
        "region": news.region,
        "countries": news.countries.split(",") if news.countries else [],
        "event_type": news.event_type,
        "market_sentiment": news.market_sentiment,
        "affected_sectors": news.affected_sectors.split(",") if news.affected_sectors else []
    }
