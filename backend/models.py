from sqlalchemy import Column, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class NewsArticle(Base):
    __tablename__ = 'news_articles'
    id = Column(String, primary_key=True)
    title = Column(String)
    content = Column(Text)
    source = Column(String)
    publish_date = Column(DateTime)
    relevance_score = Column(Float)
    region = Column(String)
    countries = Column(String)  # comma-separated
    event_type = Column(String)
    market_sentiment = Column(String)
    affected_sectors = Column(String)  # comma-separated

class GeopoliticalEvent(Base):
    __tablename__ = 'geopolitical_events'
    id = Column(String, primary_key=True)
    event_type = Column(String)
    description = Column(Text)
    date = Column(DateTime)
    region = Column(String)
    countries = Column(String)
