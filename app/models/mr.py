from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.base import Base

class MR(Base):
    __tablename__ = "mr_registration"

    id = Column(Integer, primary_key=True, index=True)
    mr_id = Column(String, unique=True, index=True, nullable=False)
    mr_pswd = Column(String, nullable=False)
    mr_name = Column(String)
    mr_address = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)