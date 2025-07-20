-- database/migrations/001_initial_schema.sql

-- News Articles
CREATE TABLE news_articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    content TEXT,
    source VARCHAR(100),
    url VARCHAR(1000) UNIQUE,
    publish_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    relevance_score FLOAT,
    region VARCHAR(100),
    countries JSON,
    event_type VARCHAR(100),
    processed BOOLEAN DEFAULT FALSE,
    sentiment_score FLOAT
);

CREATE INDEX ix_news_title ON news_articles(title);
CREATE INDEX ix_news_publish_date ON news_articles(publish_date);
CREATE INDEX ix_news_region ON news_articles(region);
CREATE INDEX ix_news_event_type ON news_articles(event_type);

-- Geopolitical Events
CREATE TABLE geopolitical_events (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(100),
    region VARCHAR(100),
    countries JSON,
    severity INTEGER,
    market_impact FLOAT,
    event_date TIMESTAMP,
    description TEXT
);

CREATE INDEX ix_event_type ON geopolitical_events(event_type);
CREATE INDEX ix_event_region ON geopolitical_events(region);

-- Event-Article Link
CREATE TABLE event_article_link (
    event_id INTEGER REFERENCES geopolitical_events(id),
    article_id INTEGER REFERENCES news_articles(id),
    PRIMARY KEY (event_id, article_id)
);

-- Stock Sectors
CREATE TABLE stock_sectors (
    id SERIAL PRIMARY KEY,
    sector_name VARCHAR(100) UNIQUE,
    stock_symbols JSON,
    description TEXT
);

-- Event-Stock Impact
CREATE TABLE event_stock_impact (
    id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES geopolitical_events(id),
    sector_id INTEGER REFERENCES stock_sectors(id),
    impact_severity FLOAT,
    confidence_score FLOAT,
    historical_performance JSON
);

-- User Preferences
CREATE TABLE user_preferences (
    id SERIAL PRIMARY KEY,
    region_filters JSON,
    event_filters JSON,
    alert_threshold FLOAT
);

-- Historical Analysis
CREATE TABLE historical_analysis (
    id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES geopolitical_events(id),
    stock_impact JSON,
    analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    confidence_score FLOAT
);

-- Sample data
INSERT INTO stock_sectors (sector_name, stock_symbols, description) VALUES
('Energy', '["XOM", "CVX", "COP"]', 'Energy sector stocks'),
('Tech', '["AAPL", "MSFT", "GOOGL"]', 'Technology sector stocks'); 