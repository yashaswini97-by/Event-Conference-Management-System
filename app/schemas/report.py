from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ReportCreate(BaseModel):
    report_type: str
    title: str
    description: Optional[str] = None


class ReportResponse(BaseModel):
    id: int
    report_type: str
    title: str
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True