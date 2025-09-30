from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserBase(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    username: str


class EditUser(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
