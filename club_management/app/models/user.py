from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.db import Base
from .enums import UserRole

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(250), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    owned_clubs = relationship("Club", back_populates="owner", foreign_keys='Club.owner_id')
    club_memberships = relationship("ClubMember", back_populates="user")
    assigned_activities = relationship("ClubActivity", back_populates="assignee")