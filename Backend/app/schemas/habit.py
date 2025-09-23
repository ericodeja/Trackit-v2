from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import enum

class HabitBase(BaseModel):
    id: int

class Habit(BaseModel):
    user_id: int
    title: str
    description: Optional[str]
    frequency: str
    start_date: datetime
    end_date: Optional[datetime]
    is_completed: bool = False

class HabitUpdate(BaseModel):
    habit_id: int
    title: Optional[str]
    description: Optional[str]
    frequency: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
