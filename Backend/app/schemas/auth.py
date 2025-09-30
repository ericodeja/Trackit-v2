from pydantic import BaseModel, EmailStr

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