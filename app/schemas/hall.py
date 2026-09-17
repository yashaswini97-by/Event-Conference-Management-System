from datetime import datetime

from pydantic import BaseModel, Field


class HallCreate(BaseModel):
    hall_name: str
    capacity: int = Field(..., gt=0)
    floor: int
    availability_status: str = "AVAILABLE"


class HallUpdate(BaseModel):
    hall_name: str | None = None
    capacity: int | None = Field(None, gt=0)
    floor: int | None = None
    availability_status: str | None = None


class HallResponse(BaseModel):
    id: int
    venue_id: int
    hall_name: str
    capacity: int
    floor: int
    availability_status: str
    is_deleted: bool
    created_at: datetime

    class Config:
        from_attributes = True