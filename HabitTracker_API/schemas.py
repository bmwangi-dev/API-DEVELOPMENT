# pyrefly: ignore [missing-import]
from pydantic import BaseModel, EmailStr
from typing import List, Optional

# --- JWT Tokens ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- Habits ---
class HabitBase(BaseModel):
    title: str

class HabitCreate(HabitBase):
    pass

class HabitUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None

class HabitResponse(HabitBase):
    id: str
    completed: bool
    user_id: str

    class Config:
        from_attributes = True

# --- Users ---
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: str
    habits: List[HabitResponse] = []

    class Config:
        from_attributes = True
