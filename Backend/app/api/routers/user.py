from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.crud.user import get_profile, edit_user, delete_user
from app.schemas.user import EditUser
from app.schemas.user import User
from app.crud.user import create_new_user

router = APIRouter(prefix='/user', tags=['User'])

@router.post('/signup')
def signup_route(form_data: User) -> dict:
    return create_new_user(form_data)


@router.get('/profile')
def get_profile_route(user: dict = Depends(get_current_user)):
    return get_profile(user)

@router.patch('/edit')
def edit_name_route(data: EditUser, user: dict = Depends(get_current_user)):
    return edit_user(data, user)

@router.delete('/')
def delete_user_route(user: dict = Depends(get_current_user)):
    return delete_user(user)