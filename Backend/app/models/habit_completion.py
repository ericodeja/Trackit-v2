from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime, timezone
import app.models.habit


class HabitCompletion(Base):
    __tablename__ = 'habit_completions'

    id: Mapped[int] = mapped_column(primary_key=True)
    habit_id: Mapped[int] = mapped_column(ForeignKey('habits.id', ondelete='CASCADE'))
    completed_at: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc))

    habit: Mapped['app.models.habit.Habit'] = relationship(
        'Habit', back_populates='completions')
