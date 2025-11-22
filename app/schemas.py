from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime


# ===== User Schemas =====

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        orm_mode = True


# ===== Auth Schemas =====

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None


# ===== Post Schemas =====

class PostCreate(BaseModel):
    content: str


class PostOut(BaseModel):
    id: int
    content: str
    author_id: int
    created_at: datetime

    class Config:
        orm_mode = True


# ===== Activity Schemas =====

class ActivityOut(BaseModel):
    id: int
    message: str
    created_at: datetime

    class Config:
        orm_mode = True
