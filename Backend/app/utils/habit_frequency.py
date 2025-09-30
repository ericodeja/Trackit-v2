from fastapi import HTTPException, status
from datetime import datetime, timezone
import asyncio
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.base import engine
from app.models.habit import Habit


frequency_type = ('daily', 'weekly', 'monthly', 'yearly')


def can_complete_task(last_completed: datetime | None, end_date: datetime | None,  frequency: str):

    now = datetime.now(timezone.utc)

    if last_completed is None:
        if end_date is None:
            return True

    elif end_date is not None:
        if now > end_date:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Habit can no longer be completed (end date passed)."
            )

    elif frequency == frequency_type[0]:
        return now.date() > last_completed.date()

    elif frequency == frequency_type[1]:
        return (now.year, now.isocalendar()[1]) > (last_completed.year, last_completed.isocalendar()[1])

    elif frequency == frequency_type[2]:
        return (now.year, now.month) > (last_completed.year, last_completed.month)

    elif frequency == frequency_type[3]:
        return now.year > last_completed.year

    else:
        raise ValueError('Invalid Input')


async def habit_checker():
    while True:
        with Session(engine) as session:
            stmt = select(Habit)
            habits = session.execute(stmt).scalars().all()

            for habit in habits:
                is_eligible = can_complete_task(
                    habit.last_completed, habit.end_date, habit.frequency)

                if is_eligible:
                    habit.is_completed = False

            session.commit()

        await asyncio.sleep(15)


# Check if the user is eligible to complete the task
# Update the task is_completed status to FALSE
