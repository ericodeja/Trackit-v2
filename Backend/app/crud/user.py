from app.models.user import User
from app.models.profile_changes import ProfileChange
from app.schemas.profile_changes import ProfileChanges
from app.crud.profile_changes import add_change
from app.schemas.user import UserBase
from app.db.base import engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.security import hash_password
from fastapi import HTTPException, status

from datetime import datetime, timedelta, timezone
from app.db.db_connection import db_connection


def create_new_user(form_data) -> dict:
    hashed_password = hash_password(form_data.password)

    new_user = User(
        first_name=form_data.first_name,
        last_name=form_data.last_name,
        username=form_data.first_name,
        email=form_data.email,
        password=hashed_password
    )

    db_connection.add(new_user)

    return {'sub': new_user.id, 'username': new_user.username}


def get_profile(user):

    current_user = db_connection.get_one(User, User.id, user.get('sub'))

    return UserBase(id=current_user.id, first_name=current_user.first_name, last_name=current_user.last_name, email=current_user.email, username=current_user.username)


def edit_user(data, user):
    user_id = user.get('sub')
    with Session(engine) as session:

        # Check if User is eligible
        stmt = select(ProfileChange).where((ProfileChange.user_id == user_id) & (
            ProfileChange.field_name == 'name reset')).order_by(ProfileChange.changed_at.desc()).limit(1)
        result = session.execute(stmt).scalar_one_or_none()

        if result:
            if datetime.now(timezone.utc) < (result.changed_at + timedelta(days=30)):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail='You can only change names every 30 days')

        current_user = db_connection.get_one(User, User.id, user_id)

        old_value = f'first_name={current_user.first_name}, last_name={current_user.last_name}, username={current_user.username}'

        if data.first_name:
            current_user.first_name = data.first_name
            current_user.username = current_user.first_name
        if data.last_name:
            current_user.last_name = data.last_name

        new_value = f'first_name={current_user.first_name}, last_name={current_user.last_name}, username={current_user.username}'

        new_change = ProfileChanges(user_id=user_id, field_name='name reset',
                                   changed_by=user_id, old_value=old_value, new_value=new_value)

        add_change(new_change)

        session.commit()


def delete_user(user):
    current_user = db_connection.get_one(User, User.id, user.get('sub'))
    db_connection.delete(current_user)
