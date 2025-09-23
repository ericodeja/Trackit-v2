from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.base import engine
from app.models.habit import Habit
from app.utils.habit_frequency import can_complete_task
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
            frequency=data.frequency.lower(),
            start_date=data.start_date,
            end_date=data.end_date
        )

        session.add(new_habit)
        session.commit()

        return new_habit


def edit_habit(data):
    with Session(engine) as session:
        stmt = select(Habit).where(Habit.id == data.id)
        current_habit = session.execute(stmt).scalar_one_or_none()

        if current_habit is not None:
            current_habit.title = data.title if data.title else current_habit.title

            current_habit.description = data.description if data.description else current_habit.description

            current_habit.frequency = data.frequency if data.frequency else current_habit.frequency

            current_habit.start_date = data.start_date if data.start_date else current_habit.start_date

            current_habit.end_date = data.end_date if data.end_date else current_habit.end_date

        else:
            raise HTTPException(status_code=404)

        session.commit()
        return current_habit

def delete_habit(data):
    with Session(engine) as session:
        stmt = select(Habit).where(Habit.id == data.id)

        current_habit = session.execute(stmt).scalar_one_or_none()

        if current_habit is not None:
            session.delete(current_habit)
            session.commit()
        
        else:
            raise HTTPException(status_code=404)
        
def complete_habit(data):
    with Session(engine) as session:
        stmt = select(Habit).where(Habit.id == data.id)
        current_habit = session.execute(stmt).scalar_one_or_none()

        if current_habit is not None:
            is_eligible = can_complete_task(current_habit.last_completed, current_habit.frequency)

            if is_eligible:
                current_habit.is_completed = True
                current_habit.last_completed = datetime.now(timezone.utc)

                session.commit()
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Task is not eligible to be completed')
        
        else:
            raise HTTPException(status_code=404)