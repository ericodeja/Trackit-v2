from jose import jwt 
from datetime import datetime, timedelta, timezone
from app.core.config import settings
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.token import Token
from app.db.base import engine


def create_access_token(user):
    encode = {'sub': user.id}
    expires = datetime.now(timezone.utc) + timedelta(minutes=15)
    encode['exp'] = int(expires.timestamp())

    if not settings.SECRET_ACCESS_KEY:
        raise ValueError('Missing SECRET_ACCESS_KEY')
    if not settings.ALGORITHM:
        raise ValueError('Missing ALGORITHM')

    # Encode token details
    access_token = jwt.encode(
        encode, settings.SECRET_ACCESS_KEY, algorithm=settings.ALGORITHM)
    return access_token


def create_refresh_token(user):
    encode = {'sub': user.id}
    expires = datetime.now(timezone.utc) + timedelta(days=7)
    encode['exp'] = int(expires.timestamp())

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

def create_password_reset_token(current_user):
    encode = {'sub': str(current_user.id), 'scope': 'password_reset'}
    expires = datetime.now(timezone.utc) + timedelta(minutes=3)
    encode['exp'] = str(int(expires.timestamp()))

    
    if not settings.PASSWORD_RESET_KEY:
        raise ValueError('Missing PASSWORD_RESET_KEY')
    if not settings.ALGORITHM:
        raise ValueError('Missing ALGORITHM')
    
    password_reset_token = jwt.encode(encode, settings.PASSWORD_RESET_KEY, algorithm=settings.ALGORITHM)

    return password_reset_token

