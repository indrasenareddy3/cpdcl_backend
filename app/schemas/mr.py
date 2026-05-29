from pydantic import BaseModel

class MRListResponse(BaseModel):
    mr_id: str
    mr_name: str | None
    mr_address: str | None

    class Config:
        orm_mode = True


from pydantic import BaseModel
from datetime import date
from typing import Optional

class MRReadingFilterRequest(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class MRLocationRequest(BaseModel):
    mr_id: str