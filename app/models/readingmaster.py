from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric,Float
from datetime import datetime
from app.db.base import Base

class Reading(Base):
    __tablename__ = "readingmaster"

    id = Column(Integer, primary_key=True)
    rdng_img = Column(String)  # S3 URL
    transaction_id = Column(String, index=True)
    mr_id = Column(String, ForeignKey("mr_registration.mr_id"))
    date = Column(DateTime)

    consumer_id = Column(String(100), index=True)

    geo_lat = Column(Float)   # DOUBLE PRECISION
    geo_long = Column(Float) 

    created_at = Column(DateTime, default=datetime.utcnow)

    class Config:
        from_attributes = True