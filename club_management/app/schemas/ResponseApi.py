from typing import Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from datetime import datetime, timezone

T = TypeVar("T")

def get_utc_now():
    return datetime.now(timezone.utc)

class APIResponse(BaseModel, Generic[T]):
    statusCode: int
    error: Optional[str] = None
    message: str
    data: Optional[T] = None
    path: str
    timestamp: datetime = Field(default_factory=get_utc_now)