from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    phone_number: str
    password: str

class UserLoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    phone_number: str
    created_at: datetime
    last_modified_ts: datetime

    class Config:
        orm_mode = True

class PasswordChange(BaseModel):
    user_name: str
    current_password: str
    new_password: str