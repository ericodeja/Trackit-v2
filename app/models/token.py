from app.db.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Token(Base):
    __tablename__ = 'tokens'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]  = mapped_column(ForeignKey('users.id'))
    token: Mapped[str]
    expires: Mapped[int]

