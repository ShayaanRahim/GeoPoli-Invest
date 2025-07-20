from .database import SessionLocal
from .models import NewsArticle, GeopoliticalEvent, StockSector, EventStockImpact, UserPreferences, HistoricalAnalysis
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta

def create_news_article(**kwargs):
    session = SessionLocal()
    try:
        article = NewsArticle(**kwargs)
        session.add(article)
        session.commit()
        return article
    except SQLAlchemyError as e:
        session.rollback()
        print(f"DB Error: {e}")
        return None
    finally:
        session.close()

def bulk_insert_articles(articles):
    session = SessionLocal()
    try:
        session.bulk_save_objects([NewsArticle(**a) for a in articles])
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"DB Error: {e}")
    finally:
        session.close()

def get_news_by_region(region, limit=20):
    session = SessionLocal()
    try:
        return session.query(NewsArticle).filter_by(region=region).order_by(NewsArticle.publish_date.desc()).limit(limit).all()
    finally:
        session.close()

def get_news_by_date_range(start, end, limit=100):
    session = SessionLocal()
    try:
        return session.query(NewsArticle).filter(NewsArticle.publish_date >= start, NewsArticle.publish_date <= end).order_by(NewsArticle.publish_date.desc()).limit(limit).all()
    finally:
        session.close()

def delete_old_news(days=90):
    session = SessionLocal()
    try:
        cutoff = datetime.utcnow() - timedelta(days=days)
        session.query(NewsArticle).filter(NewsArticle.publish_date < cutoff).delete()
        session.commit()
    finally:
        session.close()

# Add more CRUD and batch operations as needed... 