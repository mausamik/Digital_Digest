from app.db.models import Article
from app.db import database
from fastapi import FastAPI
from app.ingestion.article_fetcher import fetch_articles
from app.db import models
from app.db.database import engine
app = FastAPI(title="AutoDigital Digest", version="1.0.0")


#create a table 
models.Base.metadata.create_all(bind=database.engine)
@app.get("/")
def health_check():
    return {"status": "ok", "message": "AutoDigital Digest is running!"}

#temporary ingestion for testing purposes 
"""
id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    text = Column(Text)
    word_count = Column(Integer)
    url = Column(String, unique=True, index=True)
    used = Column(Boolean, default=False)
"""
@app.get("/ingest")
def ingest_articles():
    db = database.SessionLocal()
    articles = fetch_articles()
    saved = 0 

    for a in articles:
        exists = db.query(models.Article).filter(models.Article.url == a['url']).first()
        if exists:
            continue

        article = Article(
            title=a['title'],
            text=a['text'],
            word_count=a['word_count'],
            url=a['url']
           
        )
        db.add(article)
        saved += 1

    response =  {
        "saved_articles": saved,
        "total_fetched": len(articles)
    }
    db.commit()
    db.close()
    return response 
    

@app.get("/today")
def get_today_article(min_words: int = 300):
    db = database.SessionLocal()

    article = (
        db.query(models.Article)
        .filter(models.Article.used == False)
        .filter(models.Article.word_count >= min_words)
        .order_by(models.Article.id)
        .first()
    )

    if not article:
        db.close()
        return {"message": "No unread articles available"}

    article.used = True
    response =  {
        "title": article.title,
        "word_count": article.word_count,
        "url": article.url,
        "text": article.text[:500] + "..." if len(article.text) > 500 else article.text
    }

    db.commit()
    db.close()
    return response

    