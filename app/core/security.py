from passlib.context import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError
from app.core.config import settings
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        if not settings.SECRET_ACCESS_KEY:
            raise ValueError('Missing PASSWORD_RESET_KEY')
        if not settings.ALGORITHM:
            raise ValueError('Missing ALGORITHM')
        
        payload = jwt.decode(token, settings.SECRET_ACCESS_KEY, algorithms=[settings.ALGORITHM])
        user_id= payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return {"sub": int(user_id)}

def verify_password_reset_token(token:str):
    try:
        if not settings.RESET_KEY:
            raise ValueError('Missing RESET_KEY')
        if not settings.ALGORITHM:
            raise ValueError('Missing ALGORITHM')
        
        # Decode token
        payload = jwt.decode(token, settings.RESET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get('scope') != 'password_reset':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')

        user_id = payload.get('sub')
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token: no user ID found")
        return int(user_id)
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token expired")
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def verify_email_reset_token(token:str):
    try:
        if not settings.RESET_KEY:
            raise ValueError('Missing RESET_KEY')
        if not settings.ALGORITHM:
            raise ValueError('Missing ALGORITHM')
        
        # Decode token
        payload = jwt.decode(token, settings.RESET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get('scope') != 'email_reset':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')


        user_id = payload.get('sub')
        new_email = payload.get('new_email')

        # Check if new_email and User_id is not None
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token: no user ID found")
        if new_email is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token: no Email found")
        
        return [user_id, new_email]
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token expired")
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid or expired token")



