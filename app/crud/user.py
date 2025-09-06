from app.models.user import User
from app.models.token import Token
from app.schemas.user import UserBase
from app.db.base import engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.security import hash_password, verify_password
from fastapi import HTTPException, status
from app.crud.token import create_access_token, create_refresh_token


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
        stmt = select(User).where(User.email == form_data.email)
        current_user = session.execute(stmt).scalar_one_or_none()

        if current_user is not None:
            # Verify if password is correct
            if not verify_password(form_data.password, current_user.password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid password')

            return create_access_token(current_user), create_refresh_token(current_user)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found')


def user_logout(user):
    with Session(engine) as session:
        stmt = select(Token).where(Token.user_id == user.id)
        result = session.execute(stmt).scalar_one_or_none()
        if result is not None:
            session.delete(result)
            session.commit()
