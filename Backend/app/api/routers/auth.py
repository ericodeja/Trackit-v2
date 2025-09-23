from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import User, UserBase, PasswordResetRequest, PasswordResetConfirm, EmailResetRequest, EmailResetConfirm, EditName
from app.crud.user import create_new_user, user_login, user_logout, password_reset_request, reset_password, email_reset_request, reset_email, edit_name
from app.core.security import verify_password_reset_token, get_current_user, verify_email_reset_token

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/signup')
def signup_route(form_data: User) -> UserBase:
    return create_new_user(form_data)


@router.post('/login')
def login_route(form_data: OAuth2PasswordRequestForm = Depends()):
    return user_login(form_data)


@router.post('/logout')
def logout_route(user: dict = Depends(get_current_user)):
    return user_logout(user)

# PROFILE MANAGEMENT
@router.post('/password-reset/request')
def reset_password_request_route(data: PasswordResetRequest, background_tasks: BackgroundTasks):
    password_reset_request(data, background_tasks)
    return {"message": f"If {data.email} exists, a reset link has been sent."}


@router.post('/password-reset/confirm')
def reset_password_route(data: PasswordResetConfirm):

    user_id = verify_password_reset_token(data.token)

    if user_id is None:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    # hash new password and update db
    reset_password(user_id, data.new_password)

    return {"message": "Password reset successful"}


@router.post('/email-reset/request')
def reset_email_request_route(data: EmailResetRequest, background_tasks: BackgroundTasks, user: dict = Depends(get_current_user)):
    email_reset_request(data, user, background_tasks)


@router.post('/email-reset/confirm')
def reset_email_route(data: EmailResetConfirm, background_tasks: BackgroundTasks):
    reset_data = verify_email_reset_token(data.token)
     
    for item in  reset_data:
        if item is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    
    print(reset_data[0], reset_data[1])
    
    reset_email(reset_data[0], reset_data[1], background_tasks)

    return {"message": "Email reset successful"}

@router.patch('/edit-name')
def edit_name_route(data: EditName, user: dict = Depends(get_current_user)):
    return edit_name(data, user)
