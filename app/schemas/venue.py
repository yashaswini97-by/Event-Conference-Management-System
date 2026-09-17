from datetime import datetime
from pydantic import BaseModel, Field


class VenueCreate(BaseModel):
    venue_name: str
    address: str
    city: str
    capacity: int = Field(..., gt=0)
    facilities: str | None = None
    status: str = "AVAILABLE"


class VenueUpdate(BaseModel):
    venue_name: str | None = None
    address: str | None = None
    city: str | None = None
    capacity: int | None = Field(None, gt=0)
    facilities: str | None = None
    status: str | None = None


class VenueResponse(BaseModel):
    id: int
    venue_name: str
    address: str
    city: str
    capacity: int
    facilities: str | None
    status: str
    is_deleted: bool
    created_at: datetime

    class Config:
        from_attributes = True