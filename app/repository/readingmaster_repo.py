from sqlalchemy.orm import Session
from app.models.readingmaster import Reading

def create_reading(db: Session, reading: Reading):
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return reading