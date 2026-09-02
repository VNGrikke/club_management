from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.db import Base
from .enums import MemberRole

class ClubMember(Base):
    __tablename__ = "club_members"

    club_id = Column(Integer, ForeignKey("clubs.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    
    role = Column(Enum(MemberRole), nullable=False)
    joined_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    club = relationship("Club", back_populates="members")
    user = relationship("User", back_populates="club_memberships")