# app/services/mr_service.py

from sqlalchemy.orm import Session
from app.models.mr import MR

def get_all_mrs(db: Session):
    return db.query(
        MR.mr_id,
        MR.mr_name,
        MR.mr_address
    ).all()


# app/services/mr_service.py

from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date
from app.models.mr import MR
from app.models.readingmaster import Reading


def get_mr_with_readings_and_count(
    db: Session,
    start_date: date = None,
    end_date: date = None
):
    query = db.query(MR).all()

    result = []

    for mr in query:
        reading_query = db.query(Reading).filter(Reading.mr_id == mr.mr_id)

        # ✅ Apply date filters
        if start_date and end_date:
            start_dt = datetime.combine(start_date, datetime.min.time())
            end_dt = datetime.combine(end_date, datetime.min.time()) + timedelta(days=1)

            reading_query = reading_query.filter(
                Reading.created_at >= start_dt,
                Reading.created_at < end_dt
            )

        elif start_date:
            start_dt = datetime.combine(start_date, datetime.min.time())
            end_dt = start_dt + timedelta(days=1)

            reading_query = reading_query.filter(
                Reading.created_at >= start_dt,
                Reading.created_at < end_dt
            )

        elif end_date:
            end_dt = datetime.combine(end_date, datetime.min.time()) + timedelta(days=1)

            reading_query = reading_query.filter(
                Reading.created_at < end_dt
            )

        # ✅ Count
        total_count = reading_query.count()

        # ✅ Data
        readings = reading_query.order_by(Reading.created_at.desc()).all()

        result.append({
            "mr_id": mr.mr_id,
            "mr_name": mr.mr_name,
            "mr_address": mr.mr_address,
            "total_count": total_count,
            "readings": readings
        })

    return result


# app/services/mr_service.py

# from sqlalchemy.orm import Session
# from sqlalchemy import func, case
# from app.models.mr import MR
# from app.models.readingmaster import Reading


# def get_mr_status(db: Session):
#     results = db.query(
#         MR.mr_id,
#         MR.mr_name,
#         MR.mr_address,

#         case(
#             (
#                 func.count(Reading.id) > 0,
#                 "ACTIVE"
#             ),
#             else_="INACTIVE"
#         ).label("status")

#     ).outerjoin(
#         Reading,
#         (MR.mr_id == Reading.mr_id) &
#         (Reading.geo_lat.isnot(None)) &
#         (Reading.geo_long.isnot(None))
#     ).group_by(
#         MR.mr_id,
#         MR.mr_name,
#         MR.mr_address
#     ).all()

#     return [
#         {
#             "mr_id": row.mr_id,
#             "mr_name": row.mr_name,
#             "mr_address": row.mr_address,
#             "status": row.status
#         }
#         for row in results
#     ]




from sqlalchemy.orm import Session
from sqlalchemy import func, case
from datetime import datetime
from app.models.mr import MR
from app.models.readingmaster import Reading


def get_mr_status(db: Session):
    now = datetime.utcnow()
    today_start = datetime(now.year, now.month, now.day)

    # ✅ Main query
    results = db.query(
        MR.mr_id,
        MR.mr_name,
        MR.mr_address,

        # ACTIVE if at least one record today
        case(
            (func.count(Reading.id) > 0, "ACTIVE"),
            else_="INACTIVE"
        ).label("status")

    ).outerjoin(
        Reading,
        (MR.mr_id == Reading.mr_id) &
        (Reading.created_at >= today_start) &   # ✅ TODAY filter
        (Reading.geo_lat.isnot(None)) &
        (Reading.geo_long.isnot(None))
    ).group_by(
        MR.mr_id,
        MR.mr_name,
        MR.mr_address
    ).all()

    # ✅ Convert to list
    data = [
        {
            "mr_id": row.mr_id,
            "mr_name": row.mr_name,
            "mr_address": row.mr_address,
            "status": row.status
        }
        for row in results
    ]

    # ✅ Summary counts
    total_mrs = len(data)
    active_mrs = sum(1 for row in data if row["status"] == "ACTIVE")
    inactive_mrs = total_mrs - active_mrs

    return {
        "summary": {
            "total_mrs": total_mrs,
            "active_mrs": active_mrs,
            "inactive_mrs": inactive_mrs
        },
        "data": data
    }
# app/services/mr_service.py
# app/services/mr_service.py

from sqlalchemy.orm import Session
from datetime import datetime
from app.models.readingmaster import Reading


def get_latest_location_today(db: Session, mr_id: str):
    now = datetime.utcnow()
    today_start = datetime(now.year, now.month, now.day)

    record = (
        db.query(Reading)
        .filter(
            Reading.mr_id == mr_id,
            Reading.created_at >= today_start,
            Reading.geo_lat.isnot(None),
            Reading.geo_long.isnot(None)
        )
        .order_by(Reading.created_at.desc())
        .first()
    )

    if not record:
        return {
            "mr_id": mr_id,
            "status": "No data found for today"
        }

    return {
        "mr_id": mr_id,
        "geo_lat": record.geo_lat,
        "geo_long": record.geo_long,
        "timestamp": record.created_at
    }