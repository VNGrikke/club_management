from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.db import Base
from .enums import ActivityStatus, ActivityPriority

class ClubActivity(Base):
    __tablename__ = "club_activities"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    club_id = Column(Integer, ForeignKey("clubs.id"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    status = Column(Enum(ActivityStatus), default=ActivityStatus.TODO, nullable=False)
    priority = Column(Enum(ActivityPriority), default=ActivityPriority.MEDIUM, nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    club = relationship("Club", back_populates="activities")
    assignee = relationship("User", back_populates="assigned_activities")