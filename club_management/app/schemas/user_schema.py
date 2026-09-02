from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional
from datetime import datetime
from models.enums import UserRole

class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=100)

class UserCreate(UserBase):
    password: str  = Field(..., min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str  = Field(..., min_length=8)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)    
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8)

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)