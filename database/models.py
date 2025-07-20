from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, JSON, Index
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class NewsArticle(Base):
    __tablename__ = 'news_articles'
    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False, index=True)
    content = Column(Text)
    source = Column(String(100), index=True)
    url = Column(String(1000), unique=True)
    publish_date = Column(DateTime, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    relevance_score = Column(Float)
    region = Column(String(100), index=True)
    countries = Column(JSON)
    event_type = Column(String(100), index=True)
    processed = Column(Boolean, default=False)
    sentiment_score = Column(Float)
    # Relationships
    events = relationship('GeopoliticalEvent', secondary='event_article_link', back_populates='articles')

class GeopoliticalEvent(Base):
    __tablename__ = 'geopolitical_events'
    id = Column(Integer, primary_key=True)
    event_type = Column(String(100), index=True)
    region = Column(String(100), index=True)
    countries = Column(JSON)
    severity = Column(Integer)
    market_impact = Column(Float)
    event_date = Column(DateTime, index=True)
    description = Column(Text)
    # Relationships
    articles = relationship('NewsArticle', secondary='event_article_link', back_populates='events')
    stock_impacts = relationship('EventStockImpact', back_populates='event')

class EventArticleLink(Base):
    __tablename__ = 'event_article_link'
    event_id = Column(Integer, ForeignKey('geopolitical_events.id'), primary_key=True)
    article_id = Column(Integer, ForeignKey('news_articles.id'), primary_key=True)

class StockSector(Base):
    __tablename__ = 'stock_sectors'
    id = Column(Integer, primary_key=True)
    sector_name = Column(String(100), unique=True, index=True)
    stock_symbols = Column(JSON)
    description = Column(Text)
    impacts = relationship('EventStockImpact', back_populates='sector')

class EventStockImpact(Base):
    __tablename__ = 'event_stock_impact'
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('geopolitical_events.id'))
    sector_id = Column(Integer, ForeignKey('stock_sectors.id'))
    impact_severity = Column(Float)
    confidence_score = Column(Float)
    historical_performance = Column(JSON)
    event = relationship('GeopoliticalEvent', back_populates='stock_impacts')
    sector = relationship('StockSector', back_populates='impacts')

class UserPreferences(Base):
    __tablename__ = 'user_preferences'
    id = Column(Integer, primary_key=True)
    region_filters = Column(JSON)
    event_filters = Column(JSON)
    alert_threshold = Column(Float)

class HistoricalAnalysis(Base):
    __tablename__ = 'historical_analysis'
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('geopolitical_events.id'))
    stock_impact = Column(JSON)
    analysis_date = Column(DateTime, default=datetime.utcnow)
    confidence_score = Column(Float)
    event = relationship('GeopoliticalEvent')

# Indexes for performance
Index('ix_news_title', NewsArticle.title)
Index('ix_news_publish_date', NewsArticle.publish_date)
Index('ix_news_region', NewsArticle.region)
Index('ix_news_event_type', NewsArticle.event_type)
Index('ix_event_type', GeopoliticalEvent.event_type)
Index('ix_event_region', GeopoliticalEvent.region) 