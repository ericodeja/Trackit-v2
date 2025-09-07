from jose import jwt 
from datetime import datetime, timedelta, timezone
from app.core.config import settings
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.token import Token
from app.db.base import engine
from fastapi import HTTPException


def create_access_token(user):
    encode = {'sub': str(user.id)}
    expires = datetime.now(timezone.utc) + timedelta(minutes=15)
    encode['exp'] = str(int(expires.timestamp()))

    if not settings.SECRET_ACCESS_KEY:
        raise ValueError('Missing SECRET_ACCESS_KEY')
    if not settings.ALGORITHM:
        raise ValueError('Missing ALGORITHM')

    # Encode token details
    access_token = jwt.encode(
        encode, settings.SECRET_ACCESS_KEY, algorithm=settings.ALGORITHM)
    return access_token


def create_refresh_token(user):
    encode = {'sub': str(user.id)}
    expires = datetime.now(timezone.utc) + timedelta(days=7)
    encode['exp'] = str(int(expires.timestamp()))

    if not settings.SECRET_REFRESH_KEY:
        raise ValueError('Missing SECRET_REFRESH_KEY')
    if not settings.ALGORITHM:
        raise ValueError('Missing ALGORITHM')

    # Encode token details
    refresh_token = jwt.encode(
        encode, settings.SECRET_REFRESH_KEY, algorithm=settings.ALGORITHM)

    # Create new token object and add to database
    with Session(engine) as session:

        # Select old token if it exists
        stmt = select(Token).where(Token.user_id == user.id)
        old_token = session.execute(stmt).scalar_one_or_none()

        # Delete old token if it exists
        if old_token is not None:
            session.delete(old_token)

        # Create new token object
        new_token = Token(
            user_id=user.id,
            token=refresh_token,
            expires=int(expires.timestamp())
        )

        # Add token to database
        session.add(new_token)
        session.commit()
    return refresh_token

def create_password_reset_token(user):
    encode = {'sub': str(user.id), 'scope': 'password_reset'}
    expires = datetime.now(timezone.utc) + timedelta(minutes=3)
    encode['exp'] = str(int(expires.timestamp()))

    
    if not settings.RESET_KEY:
        raise ValueError('Missing PASSWORD_RESET_KEY')
    if not settings.ALGORITHM:
        raise ValueError('Missing ALGORITHM')
    
    password_reset_token = jwt.encode(encode, settings.RESET_KEY, algorithm=settings.ALGORITHM)

    return password_reset_token

def delete_refresh_token(user):
    user_id = user.get('sub')
    with Session(engine) as session:
        stmt = select(Token).where(Token.user_id == user_id)
        result = session.execute(stmt).scalar_one_or_none()
        if result is not None:
            session.delete(result)
            session.commit()

def create_email_reset_token(user, new_email):
    user_id = user.get('sub')

    if user_id is None:
        raise HTTPException(status_code=401)
    encode = {'sub': str(user_id), 'new_email': new_email, 'scope': 'email_reset'}
    encode['exp'] = str(int((datetime.now(timezone.utc) + timedelta(minutes=15)).timestamp()))

    if not settings.RESET_KEY:
        raise ValueError('Missing PASSWORD_RESET_KEY')
    if not settings.ALGORITHM:
        raise ValueError('Missing ALGORITHM')
    
    email_reset_token = jwt.encode(encode, settings.RESET_KEY, algorithm=settings.ALGORITHM )

    return email_reset_token