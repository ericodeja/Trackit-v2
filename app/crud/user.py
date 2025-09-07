from app.models.user import User
from app.models.token import Token
from app.schemas.user import UserBase
from app.db.base import engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.security import hash_password, verify_password
from fastapi import HTTPException, status, BackgroundTasks
from app.crud.token import create_access_token, create_refresh_token, create_password_reset_token
from app.utils.email import password_reset_email




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


def password_reset_request(data, background_tasks: BackgroundTasks):
    with Session(engine) as session:
        stmt = select(User).where(User.email == data.email)
        current_user = session.execute(stmt).scalar_one_or_none()

        if current_user is not None:
            token = create_password_reset_token(current_user)
            frontend_url = 'http://127.0.0.1:8000/auth/reset_password_route'
            reset_link = f'{frontend_url}?token={token}'

            return password_reset_email(background_tasks, current_user.email,reset_link)
        
def reset_password(user_id: int,new_password: str):
    hashed_pw = hash_password(new_password)
    with Session(engine) as session:
        stmt = select(User).where(User.id == user_id)
        current_user = session.execute(stmt).scalar_one_or_none()

        if current_user is not None:
            current_user.password = hashed_pw
            
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        
        session.commit()
