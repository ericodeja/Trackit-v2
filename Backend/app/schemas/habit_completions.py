from pydantic import BaseModel
from datetime import datetime

class HabitCompletions(BaseModel):
    habit_id : int
    completed_at : datetime