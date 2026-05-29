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
    limit: int = 20


from pydantic import BaseModel
from datetime import date

class ReadingmasterFilterRequest(BaseModel):
    mr_id: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    page: int = 1
    limit: int = 20


class BillingCountRequest(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None