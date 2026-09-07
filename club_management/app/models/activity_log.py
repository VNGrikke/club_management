from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from database.db import Base

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) 
    action = Column(String(50), nullable=False) 
    target_id = Column(Integer, nullable=True)   
    details = Column(Text, nullable=True)        
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)