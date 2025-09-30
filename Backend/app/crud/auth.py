from app.crud.token import create_access_token, create_refresh_token, create_password_reset_token, delete_refresh_token, create_email_reset_token
from app.utils.email import password_reset_email, email_reset_email, email_reset_confirmation

from fastapi import HTTPException, status, BackgroundTasks
from pydantic import EmailStr
from app.core.security import hash_password, verify_password
from app.db.db_connection import db_connection
from app.models.user import User
from app.db.base import engine
from sqlalchemy.orm import Session
from app.models.profile_changes import ProfileChange
from sqlalchemy import select


def user_login(form_data):
    current_user = db_connection.get_one(User, User.email, form_data.username)

    # Verify if password is correct
    if not verify_password(form_data.password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid password')

    return {
        "access_token": create_access_token(current_user),
        "refresh_token": create_refresh_token(current_user),
        "token_type": "bearer"
    }


def password_reset_request(data, background_tasks: BackgroundTasks):

    current_user = db_connection.get_one(User, User.email, data.email)

    token = create_password_reset_token(current_user)
    frontend_url = 'http://127.0.0.1:8000/auth/reset_password_route'
    reset_link = f'{frontend_url}?token={token}'

    return password_reset_email(background_tasks, current_user.email, reset_link)


def reset_password(user_id: int, new_password: str):
    hashed_pw = hash_password(new_password)
    with Session(engine) as session:
        current_user = db_connection.get_one(User, User.id, user_id)

        current_user.password = hashed_pw

        new_change = ProfileChange(
            user_id=user_id, field_name='password reset', changed_by=user_id, old_value=None, new_value=None)

        db_connection.add(new_change)
        session.commit()


def email_reset_request(data, user, background_tasks: BackgroundTasks):
    with Session(engine) as session:
        stmt = select(User.email).where(User.email == data.new_email)
        result = session.execute(stmt).scalar()

        if result is None:
            email_reset_token = create_email_reset_token(user, data.new_email)

            frontend_url = 'http://127.0.0.1:8000/auth/email_password_route'
            reset_link = f'{frontend_url}?token={email_reset_token}'

            return email_reset_email(background_tasks, data.new_email, reset_link)


def reset_email(user_id: int, new_email: EmailStr, background_tasks: BackgroundTasks):
    with Session(engine) as session:
        current_user = db_connection.get_one(User, User.id, user_id)

        old_email = current_user.email
        current_user.email = new_email
        email_reset_confirmation(background_tasks, old_email)

        new_change = ProfileChange(user_id=user_id, field_name='email reset',
                                   changed_by=user_id, old_value=None, new_value=new_email)

        db_connection.add(new_change)
        session.commit()


def user_logout(user):
    delete_refresh_token(user)
