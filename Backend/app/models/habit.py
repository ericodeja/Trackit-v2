from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey,  Enum
from datetime import datetime
import app.models.user


class Habit(Base):
    __tablename__ = 'habits'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'))
    title: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(250), nullable=True)
    frequency: Mapped[str]
    start_date: Mapped[datetime]
    end_date: Mapped[datetime] = mapped_column(nullable=True)
    is_completed: Mapped[bool] = mapped_column(default=False)
    last_completed: Mapped[datetime] = mapped_column(nullable=True)

    user: Mapped['app.models.user.User'] = relationship(
        'User', back_populates='habit')
