from pydantic import BaseModel

class RegisterRequest(BaseModel):
    mr_id: str
    password: str
    mr_name: str
    mr_address: str

class LoginRequest(BaseModel):
    mr_id: str
    password: str