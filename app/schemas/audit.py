from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class AuditLogCreate(BaseModel):
    user_id: Optional[int] = None
    action: str
    entity_type: Optional[str] = None
    entity_id: Optional[int] = None
    description: Optional[str] = None
    status: str = "SUCCESS"


class AuditLogResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    action: str
    entity_type: Optional[str] = None
    entity_id: Optional[int] = None
    description: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True