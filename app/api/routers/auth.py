from fastapi import APIRouter
from app.schemas.user import User, UserBase, UserLog
from app.crud.user import create_new_user, user_login, user_logout

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
