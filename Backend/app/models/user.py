from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
import app.models.token
import app.models.profile_changes
import app.models.habit


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    role: Mapped[str] = mapped_column(default='user')

    habit: Mapped['app.models.habit.Habit'] = relationship('Habit',
                                                           back_populates='user', cascade='all, delete-orphan', passive_deletes=True)

    token: Mapped['app.models.token.Token'] = relationship('Token',
                                                           back_populates='user', cascade='all, delete-orphan', passive_deletes=True)

    profile_change: Mapped['app.models.profile_changes.ProfileChange'] = relationship('ProfileChange',
                                                                                      back_populates='user',
                                                                                      foreign_keys=[app.models.profile_changes.ProfileChange.user_id], cascade='all, delete-orphan', passive_deletes=True)
