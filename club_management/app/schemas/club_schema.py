from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ClubBase(BaseModel):
    name: str
    description: Optional[str] = None

class ClubCreate(ClubBase):
    owner_id: int 

class ClubUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    owner_id: Optional[int] = None

class ClubResponse(ClubBase):
    id: int
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)