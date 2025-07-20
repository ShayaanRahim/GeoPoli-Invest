import os
import json
from sqlalchemy.exc import SQLAlchemyError
from database.database import engine, SessionLocal
from database.models import NewsArticle

def validate_article_data(data):
    required = ['title', 'url', 'publish_date']
    for field in required:
        if not data.get(field):
            return False
    return True

def is_duplicate_article(url):
    session = SessionLocal()
    try:
        return session.query(NewsArticle).filter_by(url=url).first() is not None
    finally:
        session.close()

def backup_db(backup_path='backup.sql'):
    with engine.connect() as conn:
        with open(backup_path, 'w') as f:
            for line in conn.connection.iterdump():
                f.write('%s\n' % line)

def restore_db(backup_path='backup.sql'):
    with engine.connect() as conn:
        with open(backup_path, 'r') as f:
            sql = f.read()
            conn.execute(sql)

def log_slow_query(query, duration, threshold=1.0):
    if duration > threshold:
        print(f"Slow query ({duration:.2f}s): {query}")

# Add more helpers as needed... 