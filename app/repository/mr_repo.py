from sqlalchemy.orm import Session
from app.models.mr import MR

def get_by_mr_id(db: Session, mr_id: str):
    return db.query(MR).filter(MR.mr_id == mr_id).first()

def create_user(db: Session, user: MR):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user