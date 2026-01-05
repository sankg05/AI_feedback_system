from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .db import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)

    rating = Column(Integer, nullable=False)
    review_text = Column(Text, nullable=True)

    ai_user_response = Column(Text, nullable=True)
    ai_summary = Column(Text, nullable=True)
    ai_recommended_actions = Column(Text, nullable=True)

    status = Column(String(50), default="processed")
    error_message = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    

