from sqlalchemy import Column, Integer, String, Text, Boolean
from app.db.database import Base

class Article(Base):
    __tablename__ = "digital_digest"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    text = Column(Text)
    word_count = Column(Integer)
    url = Column(String, unique=True, index=True)
    used = Column(Boolean, default=False)