from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from models.enums import ActivityStatus, ActivityPriority

class ClubActivityBase(BaseModel):
    title: str
    description: Optional[str] = None
    assignee_id: Optional[int] = None
    status: ActivityStatus = ActivityStatus.TODO
    priority: ActivityPriority = ActivityPriority.MEDIUM
    due_date: Optional[datetime] = None

class ClubActivityCreate(ClubActivityBase):
    pass

class ClubActivityUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assignee_id: Optional[int] = None
    status: Optional[ActivityStatus] = None
    priority: Optional[ActivityPriority] = None
    due_date: Optional[datetime] = None

class ClubActivityResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None 
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class DetailClubActivityResponse(ClubActivityBase):
    id: int
    created_at: datetime 

    model_config = ConfigDict(from_attributes=True) 