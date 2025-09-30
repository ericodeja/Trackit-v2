from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.base import engine
from app.models.habit import Habit
from app.utils.habit_frequency import can_complete_task
from datetime import datetime, timedelta, timezone
from app.crud.habit_completions import add_completion
from app.schemas.habit_completions import HabitCompletions
from app.db.db_connection import db_connection


def create_habit(data, user):
    user_id = user.get('sub')
    if data.start_date <= datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date must be in the future"
        )
    else:
        data.start_date.replace(
            tzinfo=timezone.utc) if data.start_date.tzinfo is None else data.start_date

    if data.end_date:
        if data.end_date < (datetime.now(timezone.utc) + timedelta(days=2)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="end_date must be in the future"
            )
        data.end_date.replace(
            tzinfo=timezone.utc) if data.end_date.tzinfo is None else data.end_date

    new_habit = Habit(
        user_id=user_id,
        title=data.title,
        description=data.description if data.description else '',
        frequency=data.frequency.lower(),
        start_date=data.start_date,
        end_date=data.end_date
    )

    db_connection.add(new_habit)

    return new_habit


def get_all_habits(user):
    with Session(engine) as session:
        stmt = select(Habit).where(Habit.user_id == user.get('sub'))
        result = session.execute(stmt).scalars().all()

        return result


def edit_habit(data):
    with Session(engine) as session:
        stmt = select(Habit).where(Habit.id == data.habit_id)
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
    current_habit = db_connection.get_one(Habit, Habit.id, data.id)
    db_connection.delete(current_habit)


def complete_habit(data):
    with Session(engine) as session:
        stmt = select(Habit).where(Habit.id == data.id)
        current_habit = session.execute(stmt).scalar_one_or_none()

        if current_habit is None:
            raise HTTPException(status_code=404)

        is_eligible = can_complete_task(
            current_habit.last_completed, current_habit.end_date, current_habit.frequency)

        if is_eligible:
            current_habit.is_completed = True
            current_habit.last_completed = datetime.now(timezone.utc)

            new_completion = HabitCompletions(
                habit_id=current_habit.id,
                completed_at=datetime.now(timezone.utc)
            )
            add_completion(new_completion)

            session.commit()
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail='Task is not eligible to be completed')
