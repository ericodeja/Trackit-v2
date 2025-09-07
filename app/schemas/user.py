from pydantic import BaseModel, EmailStr

class User(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class UserBase(BaseModel):
    id: int
    username: str

class UserLog(BaseModel):
    email: EmailStr
    password: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

class EmailResetRequest(BaseModel):
    new_email: EmailStr

class EmailResetConfirm(BaseModel):
    token: str