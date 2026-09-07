from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class ClubBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Tên câu lạc bộ")
    description: Optional[str] = None

class ClubCreate(ClubBase):
    pass 

class ClubUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None

class ClubResponse(ClubBase):
    id: int
    owner_id: int
    created_at: datetime
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)