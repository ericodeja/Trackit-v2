from passlib.context import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError
from app.core.config import settings
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def verify_password_reset_token(token:str):
    try:
        if not settings.PASSWORD_RESET_KEY:
            raise ValueError('Missing PASSWORD_RESET_KEY')
        if not settings.ALGORITHM:
            raise ValueError('Missing ALGORITHM')
        
        # Decode token
        payload = jwt.decode(token, settings.PASSWORD_RESET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get('scope') != 'password_reset':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')

        user_id = payload.get('sub')
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token: no user ID found")
        return int(user_id)
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token expired")
    except JWTError as e:
        print(f"JWT error: {e}")
