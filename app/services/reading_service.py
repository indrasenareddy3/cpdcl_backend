from app.models.readingmaster import Reading
from app.repository.readingmaster_repo import create_reading
from fastapi import HTTPException


def add_reading(db, data):
    try:
        reading = Reading(
            rdng_img=data.rdng_img,
            transaction_id=data.transaction_id,
            mr_id=data.mr_id,
            consumer_id=data.consumer_id,
            date=data.date,
            geo_lat=data.geo_lat,
            geo_long=data.geo_long
        )

        created = create_reading(db, reading)

        return {
            "status": True,
            "message": "Reading inserted successfully",
            "data": {
                "id": created.id,
                "transaction_id": created.transaction_id,
                "mr_id":created.mr_id,
                "rdng_img":created.rdng_img,
            }
        }

    except Exception as e:
        db.rollback()  # ✅ very important

        raise HTTPException(
            status_code=500,
            detail=f"Insertion failed: {str(e)}"
        )


from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime



def get_reading_counts(db: Session, mr_id: str):
    now = datetime.utcnow()

    today_start = datetime(now.year, now.month, now.day)
    month_start = datetime(now.year, now.month, 1)

    if now.month == 1:
        last_month_start = datetime(now.year - 1, 12, 1)
    else:
        last_month_start = datetime(now.year, now.month - 1, 1)

    last_month_end = month_start

    today_count = db.query(func.count(Reading.id)).filter(
        Reading.mr_id == mr_id,
        Reading.created_at >= today_start
    ).scalar()

    month_count = db.query(func.count(Reading.id)).filter(
        Reading.mr_id == mr_id,
        Reading.created_at >= month_start
    ).scalar()

    last_month_count = db.query(func.count(Reading.id)).filter(
        Reading.mr_id == mr_id,
        Reading.created_at >= last_month_start,
        Reading.created_at < last_month_end
    ).scalar()

    return {
        "mr_id": mr_id,
        "today_count": today_count,
        "this_month_count": month_count,
        "last_month_count": last_month_count
    }




from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session
from app.models.readingmaster import Reading


def get_all_readings(
    db: Session,
    mr_id: str = None,
    start_date: date = None,   
    end_date: date = None,    
    skip: int = 0,
    limit: int = 20
):
    query = db.query(Reading)

    if mr_id:
        query = query.filter(Reading.mr_id == mr_id)

    # ✅ Case 1: both start_date and end_date
    if start_date and end_date:
        start_dt = datetime.combine(start_date, datetime.min.time())
        end_dt = datetime.combine(end_date, datetime.min.time()) + timedelta(days=1)

        query = query.filter(
            Reading.created_at >= start_dt,
            Reading.created_at < end_dt   # 👈 important (< not <=)
        )

    # ✅ Case 2: only start_date
    elif start_date:
        start_dt = datetime.combine(start_date, datetime.min.time())
        end_dt = start_dt + timedelta(days=1)

        query = query.filter(
            Reading.created_at >= start_dt,
            Reading.created_at < end_dt
        )

    # ✅ Case 3: only end_date
    elif end_date:
        end_dt = datetime.combine(end_date, datetime.min.time()) + timedelta(days=1)

        query = query.filter(
            Reading.created_at < end_dt
        )

    return (
        query
        .order_by(Reading.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session
from app.models.readingmaster import Reading


def get_all_mr_readings(
    db: Session,
    mr_id: str = None,
    start_date: date = None,
    end_date: date = None,
    page: int = 1,
    limit: int = 20
):
    query = db.query(Reading)

    if mr_id:
        query = query.filter(Reading.mr_id == mr_id)

    # ✅ Date filters
    if start_date and end_date:
        start_dt = datetime.combine(start_date, datetime.min.time())
        end_dt = datetime.combine(end_date, datetime.min.time()) + timedelta(days=1)

        query = query.filter(
            Reading.created_at >= start_dt,
            Reading.created_at < end_dt
        )

    elif start_date:
        start_dt = datetime.combine(start_date, datetime.min.time())
        end_dt = start_dt + timedelta(days=1)

        query = query.filter(
            Reading.created_at >= start_dt,
            Reading.created_at < end_dt
        )

    elif end_date:
        end_dt = datetime.combine(end_date, datetime.min.time()) + timedelta(days=1)

        query = query.filter(
            Reading.created_at < end_dt
        )

    # ✅ Total count
    total_count = query.count()

    # ✅ Convert page → skip
    skip = (page - 1) * limit

    # ✅ Paginated data
    data = (
        query
        .order_by(Reading.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "total_count": total_count,
        "page": page,
        "page_size": limit,
        "total_pages": (total_count + limit - 1) // limit,
        "data": data
    }



from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta, date
from app.models.readingmaster import Reading


def get_billing_counts(
    db: Session,
    start_date: date = None,
    end_date: date = None
):
    now = datetime.utcnow()

    # ✅ Today
    today_start = datetime(now.year, now.month, now.day)
    today_end = today_start + timedelta(days=1)

    # ✅ This month
    month_start = datetime(now.year, now.month, 1)

    # ✅ Last month
    if now.month == 1:
        last_month_start = datetime(now.year - 1, 12, 1)
    else:
        last_month_start = datetime(now.year, now.month - 1, 1)

    last_month_end = month_start

    # ✅ Custom range
    start_dt = None
    end_dt = None

    if start_date:
        start_dt = datetime.combine(start_date, datetime.min.time())

    if end_date:
        end_dt = datetime.combine(end_date, datetime.min.time()) + timedelta(days=1)

    # ✅ Build conditions safely
    conditions = []

    if start_dt:
        conditions.append(Reading.created_at >= start_dt)

    if end_dt:
        conditions.append(Reading.created_at < end_dt)

    result = db.query(

        # Today
        func.count().filter(
            Reading.created_at >= today_start,
            Reading.created_at < today_end
        ).label("today_count"),

        # This month
        func.count().filter(
            Reading.created_at >= month_start
        ).label("this_month_count"),

        # Last month
        func.count().filter(
            Reading.created_at >= last_month_start,
            Reading.created_at < last_month_end
        ).label("last_month_count"),

        # Custom range
        func.count().filter(*conditions).label("custom_range_count")

    ).one()

    return {
        "today_count": result.today_count,
        "this_month_count": result.this_month_count,
        "last_month_count": result.last_month_count,
        "custom_range_count": result.custom_range_count
    }