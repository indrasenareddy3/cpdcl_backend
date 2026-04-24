from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReadingCreate(BaseModel):
    rdng_img: str
    transaction_id: str
    mr_id: str
    date: datetime
    geo_lat: float
    geo_long: float


class ReadingResponse(BaseModel):
    id: int
    rdng_img: str
    transaction_id: str
    mr_id: str
    date: datetime
    geo_lat: float
    geo_long: float
    created_at: datetime

    class Config:
        from_attributes = True 


class ReadingStatsRequest(BaseModel):
    mr_id: str


class ReadingFilterRequest(BaseModel):
    mr_id: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    skip: int = 0
    limit: int = 10