# app/api/routes/mr.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db
from app.schemas.mr import MRListResponse, MRReadingFilterRequest, MRLocationRequest
from app.services.mr_service import get_all_mrs,get_mr_with_readings_and_count, get_mr_status, get_latest_location_today

router = APIRouter(prefix="/mr", tags=["MR"])

@router.get("/mr_list", response_model=List[MRListResponse])
def get_mr_list(db: Session = Depends(get_db)):
    return get_all_mrs(db)



@router.post("/mr_readings_summary")
def get_mr_readings_summary(
    data: MRReadingFilterRequest,
    db: Session = Depends(get_db)
):
    return get_mr_with_readings_and_count(
        db=db,
        start_date=data.start_date,
        end_date=data.end_date
    )

@router.get("/status")
def get_mr_status_api(db: Session = Depends(get_db)):
    return get_mr_status(db)


@router.post("/latest-location")
def get_latest_location(
    data: MRLocationRequest,
    db: Session = Depends(get_db)
):
    return get_latest_location_today(db, data.mr_id)