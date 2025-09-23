from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.base import engine
from app.models.habit_completion import HabitCompletion


def add_completion(data):
    with Session(engine) as session:
        new_completion = HabitCompletion(
            habit_id = data.habit_id,
            completed_at = data.completed_at
        )

        session.add(new_completion)
        session.commit()
    
def get_completion(habit_id):
    with Session(engine) as session:
        stmt = select(HabitCompletion).where(HabitCompletion.habit_id == habit_id)
        result = session.execute(stmt).scalars().all()

        return result