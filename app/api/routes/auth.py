from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.auth import RegisterRequest, LoginRequest
from app.services.auth_service import register, login
from app.api.deps import get_db

router = APIRouter(prefix="/auth")

@router.post("/register")
def register_api(data: RegisterRequest, db: Session = Depends(get_db)):
    return register(db, data)

@router.post("/login")
def login_api(data: LoginRequest, db: Session = Depends(get_db)):
    return login(db, data)

@router.post("/logout")
def logout():
    try:
        return {
            "success": True,
            "message": "Logout successful"
        }
    except Exception:
        return {
            "success": False,
            "message": "Logout failed"
        }