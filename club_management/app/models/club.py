from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.db import Base

class Club(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    is_deleted = Column(Boolean, default=False, nullable=False)

    owner = relationship("User", back_populates="owned_clubs", foreign_keys=[owner_id])
    members = relationship("ClubMember", back_populates="club")
    activities = relationship("ClubActivity", back_populates="club")