from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from app.schemas.user import User, UserBase, UserLog, PasswordResetRequest, PasswordResetConfirm
from app.crud.user import create_new_user, user_login, user_logout, password_reset_request, reset_password
from app.core.security import verify_password_reset_token

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/signup')
def signup_route(form_data: User) -> UserBase:
    return create_new_user(form_data)


@router.post('/login')
def login_route(form_data: UserLog):
    return user_login(form_data)


@router.post('/logout')
def logout_route(user: UserBase):
    return user_logout(user)


@router.post('/password-reset-request')
def reset_password_request_route(data: PasswordResetRequest, background_tasks: BackgroundTasks):
    password_reset_request(data, background_tasks)
    return {"message": f"If {data.email} exists, a reset link has been sent."}


@router.patch("/reset-password")
def reset_password_route(data: PasswordResetConfirm):

    user_id =   verify_password_reset_token(data.token)

    if user_id is None:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    # hash new password and update db
    reset_password(user_id, data.new_password)

    return {"message": "Password reset successful"}
