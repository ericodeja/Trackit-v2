from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from datetime import date
import app.models.user

class Habit(Base):
    __tablename__ = 'habits'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    title: Mapped[str] = mapped_column(String(30))
    Description: Mapped[str] = mapped_column(String(250), nullable=True)
    Frequency: Mapped[str]
    start_date: Mapped[date]
    end_date: Mapped[date]

    user: Mapped['app.models.user.User'] = relationship('User', back_populates='habit')