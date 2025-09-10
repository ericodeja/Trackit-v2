from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    username: Mapped[str]
    email:Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    role: Mapped[str] = mapped_column(default='user')
