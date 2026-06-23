from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime

# ── User 스키마 ──────────────────────────────────
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(..., min_length=4)

    @field_validator("username") #aafbad123, 
    @classmethod
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError("영문자/숫자만 가능합니다.")
        return v
    
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    model_config = {"from_attributes": True}  #ORM 객체 자동 변환
    

# ── Item 스키마 ──────────────────────────────────
class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None


class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    owner_id: Optional[int] = None
    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None
