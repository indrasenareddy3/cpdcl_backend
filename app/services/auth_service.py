from fastapi import HTTPException
from app.repository.mr_repo import get_by_mr_id, create_user
from app.core.security import hash_password, verify_password, create_token
from app.models.mr import MR

def register(db, data):
    if get_by_mr_id(db, data.mr_id):
        raise HTTPException(400, "User exists")

    user = MR(
        mr_id=data.mr_id,
        mr_pswd=hash_password(data.password),
        mr_name=data.mr_name,
        mr_address=data.mr_address
    )
    return create_user(db, user)

def login(db, data):
    user = get_by_mr_id(db, data.mr_id)

    if not user or not verify_password(data.password, user.mr_pswd):
        raise HTTPException(401, "Invalid credentials")

    # return {"access_token": create_token({"sub": user.mr_id})}
    return {
        "message": "Login successful",
        "access_token": create_token({"sub": user.mr_id}),
        "token_type": "bearer"
    }