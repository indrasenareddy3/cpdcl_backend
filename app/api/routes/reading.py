from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.readingmaster import ReadingCreate
from app.services.reading_service import add_reading
from app.api.deps import get_db
from app.services.reading_service import get_reading_counts

from app.services.reading_service import get_all_readings,get_all_mr_readings,get_billing_counts
from app.schemas.readingmaster import ReadingResponse,ReadingStatsRequest,ReadingFilterRequest,ReadingmasterFilterRequest,BillingCountRequest
from typing import List

router = APIRouter(prefix="/reading", tags=["Reading"])

@router.post("/create")
def create_reading_api(data: ReadingCreate, db: Session = Depends(get_db)):
    return add_reading(db, data)




# @router.get("/pod_count")
# def reading_stats(db: Session = Depends(get_db)):
#     return get_reading_counts(db)


@router.post("/mr_pod_count")
def reading_stats(data: ReadingStatsRequest, db: Session = Depends(get_db)):
    return get_reading_counts(db, data.mr_id)

# @router.get("/pod_all", response_model=List[ReadingResponse])
# def get_readings(
#     skip: int = Query(0, ge=0),
#     limit: int = Query(10, le=100),
#     db: Session = Depends(get_db)
# ):
#     return get_all_readings(db, skip, limit)


@router.post("/mr_pods", response_model=List[ReadingResponse])
def get_readings(
    data: ReadingFilterRequest,
    db: Session = Depends(get_db)
):
    return get_all_readings(
        db=db,
        mr_id=data.mr_id,
        start_date=data.start_date,
        end_date=data.end_date,
        skip=data.skip,
        limit=data.limit
    )


@router.post("/all_mr_pods")
def get_all_mr_readings_api(
    data: ReadingmasterFilterRequest,
    db: Session = Depends(get_db)
):
    return get_all_mr_readings(
        db=db,
        mr_id=data.mr_id,
        start_date=data.start_date,
        end_date=data.end_date,
        page=data.page,
        limit=data.limit
    )


from typing import Optional
from sqlalchemy.orm import Session
from datetime import date


@router.get("/billing-counts")
def billing_counts(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    return get_billing_counts(
        db=db,
        start_date=start_date,
        end_date=end_date
    )