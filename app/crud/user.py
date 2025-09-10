from app.models.user import User
from app.schemas.user import UserBase
from app.db.base import engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import EmailStr
from app.core.security import hash_password, verify_password
from fastapi import HTTPException, status, BackgroundTasks
from app.crud.token import create_access_token, create_refresh_token,create_password_reset_token, delete_refresh_token, create_email_reset_token
from app.utils.email import password_reset_email, email_reset_email, email_reset_confirmation


def create_new_user(form_data) -> UserBase:
    hashed_password = hash_password(form_data.password)
    with Session(engine) as session:

        new_user = User(
            first_name=form_data.first_name,
            last_name=form_data.last_name,
            username=form_data.first_name,
            email=form_data.email,
            password=hashed_password
        )

        session.add(new_user)
        session.commit()

        return UserBase(id=new_user.id, username=new_user.username)


def user_login(form_data):
    with Session(engine) as session:
        stmt = select(User).where(User.email == form_data.username)
        current_user = session.execute(stmt).scalar_one_or_none()

        if current_user is not None:
            # Verify if password is correct
            if not verify_password(form_data.password, current_user.password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid password')

            return {
                "access_token": create_access_token(current_user),
                "refresh_token": create_refresh_token(current_user),
                "token_type": "bearer"
            }

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found')


def user_logout(user):
    delete_refresh_token(user)


def password_reset_request(data, background_tasks: BackgroundTasks):
    with Session(engine) as session:
        stmt = select(User).where(User.email == data.email)
        current_user = session.execute(stmt).scalar_one_or_none()

        if current_user is not None:
            token = create_password_reset_token(current_user)
            frontend_url = 'http://127.0.0.1:8000/auth/reset_password_route'
            reset_link = f'{frontend_url}?token={token}'

            return password_reset_email(background_tasks, current_user.email, reset_link)


def reset_password(user_id: int, new_password: str):
    hashed_pw = hash_password(new_password)
    with Session(engine) as session:
        stmt = select(User).where(User.id == user_id)
        current_user = session.execute(stmt).scalar_one_or_none()

        if current_user is not None:
            current_user.password = hashed_pw

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

        session.commit()

def email_reset_request(data, user, background_tasks: BackgroundTasks):
    with Session(engine) as session:
        stmt = select(User.email).where(User.email == data.new_email)
        result = session.execute(stmt).scalar()

        if result is None:
            email_reset_token = create_email_reset_token(user, data.new_email)

            frontend_url = 'http://127.0.0.1:8000/auth/email_password_route'
            reset_link = f'{frontend_url}?token={email_reset_token}'
            print(email_reset_token)

            return email_reset_email(background_tasks, data.new_email, reset_link)
        

def reset_email(user_id: int, new_email: EmailStr, background_tasks: BackgroundTasks):
    with Session(engine) as session:
        stmt = select(User).where(User.id == user_id)
        current_user = session.execute(stmt).scalar_one_or_none()

        if current_user is not None:
            old_email = current_user.email
            current_user.email = new_email
            email_reset_confirmation(background_tasks, old_email)

        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        session.commit()

def edit_name(data, user):
    user_id = user.get('sub')
    with Session(engine) as session:
        stmt = select(User).where(User.id == user_id)
        current_user = session.execute(stmt).scalar_one_or_none()

        if current_user is not None:
            if data.first_name:
                current_user.first_name = data.first_name
                current_user.username = current_user.first_name
            if data.last_name:
                current_user.last_name = data.last_name
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        
        session.commit()
