from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import engine
from app.models.habit import Habit
from datetime import datetime, timedelta, timezone


def create_habit(data, user):
    user_id = user.get('sub')
    with Session(engine) as session:
        if data.start_date <= datetime.now(timezone.utc):
            raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="start_date must be in the future"
    )
        if data.end_date:
            if data.end_date < (datetime.now(timezone.utc) + timedelta(days=2)):
                raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="end_date must be in the future"
        )
        

        new_habit = Habit(
            user_id=user_id,
            title=data.title,
            description=data.description if data.description else '',
            frequency=data.frequency,
            start_date=data.start_date,
            end_date=data.end_date 
        )

        session.add(new_habit)
        session.commit()

        return new_habit
