# backend/models/health_log.py
from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime
from database import Base

class HealthLog(Base):
    __tablename__ = "health_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)  # optional: from JWT later
    input_text = Column(String)
    status = Column(String)
    recommendations = Column(JSON)
    chart = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
