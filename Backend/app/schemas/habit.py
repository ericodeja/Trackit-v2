from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import enum



class HabitStatus(str, enum.Enum):
    COMPLETED = 'COMPLETED'
    INCOMPLETE = 'INCOMPLETE'

class Habit(BaseModel):
    user_id: int
    title: str
    description: Optional[str]
    frequency: str
    start_date: datetime
    end_date: Optional[datetime]
    status: HabitStatus = HabitStatus.INCOMPLETE